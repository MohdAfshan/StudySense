import json, random
import fitz  # PyMuPDF
import chromadb
import httpx
import ollama
from sentence_transformers import SentenceTransformer

MODEL_NAME = "llama3.1:8b"
OLLAMA_HOST = "http://localhost:11434"

llm = ollama.Client(host=OLLAMA_HOST)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = None
all_chunks = []   # list of (text, page)
page_count = 0

ANSWER_STYLES = {
    "Detailed": "Give a clear, detailed explanation.",
    "Simple (ELI5)": "Explain in very simple words for a beginner, with a short everyday example if possible.",
    "Short & to the point": "Answer in at most 3 sentences.",
    "Exam-ready bullets": "Answer as concise bullet points a student could write in an exam.",
}

SUMMARY_STYLES = {
    "Key points": "Summarize as clear bullet points covering the main ideas.",
    "Short paragraph": "Summarize in one short paragraph of about 100 words.",
    "Exam revision notes": "Write revision notes with headings and bullet points, highlighting important definitions.",
    "Explain like I'm 12": "Summarize in very simple language that a 12 year old could understand.",
}


class OllamaError(RuntimeError):
    """A user-facing error raised when the local Ollama service cannot generate text."""


def gen(prompt):
    try:
        response = llm.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"].strip()
    except ollama.ResponseError as e:
        if e.status_code == 404 or "not found" in str(e).lower():
            raise OllamaError(
                f"Ollama model '{MODEL_NAME}' is not installed. "
                f"Run 'ollama pull {MODEL_NAME}' and try again."
            ) from e
        raise OllamaError(f"Ollama returned an error: {e}") from e
    except httpx.RequestError as e:
        raise OllamaError(
            "Could not connect to Ollama at "
            f"{OLLAMA_HOST}. Make sure Ollama is running and try again."
        ) from e
    except (KeyError, TypeError) as e:
        raise OllamaError("Ollama returned an invalid response.") from e


def chunk_text(text, size=150, overlap=30):
    words = text.split()
    out, i = [], 0
    while i < len(words):
        out.append(" ".join(words[i:i + size]))
        i += size - overlap
    return out


def ingest(pdf_path):
    global collection, all_chunks, page_count
    try:
        client.delete_collection("pdf")
    except Exception:
        pass
    collection = client.create_collection("pdf")
    all_chunks = []
    ids, docs, metas = [], [], []
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    for page_no, page in enumerate(doc, start=1):
        for j, chunk in enumerate(chunk_text(page.get_text())):
            if len(chunk.split()) < 10:
                continue
            all_chunks.append((chunk, page_no))
            ids.append(f"p{page_no}_c{j}")
            docs.append(chunk)
            metas.append({"page": page_no})
    if docs:
        embeddings = embedder.encode(docs).tolist()
        collection.add(ids=ids, documents=docs, embeddings=embeddings, metadatas=metas)
    return len(all_chunks)


def ask(question, k=4, style="Detailed"):
    q_emb = embedder.encode(question).tolist()
    res = collection.query(query_embeddings=[q_emb], n_results=k)
    docs, metas = res["documents"][0], res["metadatas"][0]
    context = "\n\n".join(f"[Page {m['page']}] {d}" for d, m in zip(docs, metas))
    prompt = f"""You are a study assistant. Answer ONLY using the context below.
If the answer is not in the context, say "Not found in the document."
{ANSWER_STYLES.get(style, ANSWER_STYLES["Detailed"])}
Mention the page numbers you used.

Context:
{context}

Question: {question}"""
    answer = gen(prompt)
    pages = sorted({m["page"] for m in metas})
    return answer, pages, list(zip(docs, metas))


# ---------- helpers for the other features ----------

def _pool(page_range=None):
    """Chunks to use, optionally limited to a (start_page, end_page) range."""
    if page_range:
        lo, hi = page_range
        pool = [c for c in all_chunks if lo <= c[1] <= hi]
        if pool:
            return pool
    return all_chunks


def _spread_sample(pool, n):
    """Evenly spaced chunks so the whole document is covered."""
    if len(pool) <= n:
        return pool
    step = len(pool) / n
    return [pool[int(i * step)] for i in range(n)]


def _as_text(chunks):
    return "\n\n".join(f"[Page {p}] {c}" for c, p in chunks)


def _parse_json_list(raw):
    raw = raw.replace("```json", "").replace("```", "").strip()
    start, end = raw.find("["), raw.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON list found")
    return json.loads(raw[start:end + 1])


def _json_call(prompt, tries=2):
    last_error = None
    for _ in range(tries):
        try:
            return _parse_json_list(gen(prompt))
        except Exception as e:
            last_error = e
    raise ValueError(f"Could not get valid JSON from the model: {last_error}")


# ---------- features ----------

def summarize(style="Key points", page_range=None):
    sample = _spread_sample(_pool(page_range), 20)
    instruction = SUMMARY_STYLES.get(style, SUMMARY_STYLES["Key points"])
    prompt = f"""{instruction}
Use only the study material below.

{_as_text(sample)}"""
    return gen(prompt)


def generate_quiz(n=5, difficulty="Medium", page_range=None):
    pool = _pool(page_range)
    sample = random.sample(pool, min(len(pool), max(6, n * 2)))
    prompt = f"""Create {n} {difficulty}-level multiple-choice questions from the text below.
Rules:
- Exactly 4 options per question, written as plain text (no "A)" or "1." prefixes).
- "answer" must be EXACTLY the same text as one of the options.
- Add a one-sentence "explanation" of why the answer is correct.
- "page" is the page number the answer comes from.
Return ONLY a valid JSON list, no extra text, in this format:
[{{"question": "...", "options": ["...","...","...","..."], "answer": "...", "explanation": "...", "page": 1}}]

Text:
{_as_text(sample)}"""
    data = _json_call(prompt)
    clean = []
    for item in data:
        try:
            options = [str(o) for o in item["options"]]
            answer = str(item["answer"])
            if answer not in options:
                continue
            clean.append({
                "question": str(item["question"]),
                "options": options,
                "answer": answer,
                "explanation": str(item.get("explanation", "")),
                "page": item.get("page", "?"),
            })
        except Exception:
            continue
    if not clean:
        raise ValueError("Quiz generation failed")
    return clean[:n]


def generate_flashcards(n=8, page_range=None):
    sample = _spread_sample(_pool(page_range), 15)
    prompt = f"""Create {n} study flashcards from the text below.
Each card has a short "front" (a question or term) and a clear "back" (the answer, max 2 sentences).
Return ONLY a valid JSON list, no extra text, in this format:
[{{"front": "...", "back": "...", "page": 1}}]

Text:
{_as_text(sample)}"""
    data = _json_call(prompt)
    cards = [{"front": str(d["front"]), "back": str(d["back"]), "page": d.get("page", "?")}
             for d in data if "front" in d and "back" in d]
    if not cards:
        raise ValueError("Flashcard generation failed")
    return cards[:n]


def key_terms(n=10):
    sample = _spread_sample(all_chunks, 20)
    prompt = f"""List the {n} most important key terms from the text below, each with a one-sentence definition.
Return ONLY a valid JSON list, no extra text, in this format:
[{{"term": "...", "definition": "...", "page": 1}}]

Text:
{_as_text(sample)}"""
    data = _json_call(prompt)
    terms = [{"term": str(d["term"]), "definition": str(d["definition"]), "page": d.get("page", "?")}
             for d in data if "term" in d and "definition" in d]
    if not terms:
        raise ValueError("Key term extraction failed")
    return terms[:n]


def suggest_questions(n=5):
    sample = _spread_sample(all_chunks, 10)
    prompt = f"""Based on the text below, write {n} good questions a student could ask about it.
Each question must be answerable from the text and under 15 words.
Return ONLY a valid JSON list of strings, no extra text.

Text:
{_as_text(sample)}"""
    data = _json_call(prompt)
    return [str(q) for q in data][:n]