import os
import re
import tempfile
import time

import fitz  # PyMuPDF
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import rag
from components import ui
from styles import inject_css

st.set_page_config(page_title="StudySense", page_icon="📚", layout="wide")
inject_css()


# ---------------------------------------------------------------- state
def fresh_state():
    return {
        "loaded": None, "chunks": 0, "pages": 0, "pdf_path": None, "size_kb": None,
        "history": [], "asked": 0, "suggestions": [],
        "hits": [], "pipe": -1, "boot_map": False,
        "summary": None,
        "quiz": [], "quiz_id": 0, "result": None, "quiz_history": [],
        "cards": [],
        "terms": [],
    }


for key, value in fresh_state().items():
    st.session_state.setdefault(key, value)

S = st.session_state
SAMPLE = "sample.pdf"


def show_error(e):
    msg = str(e)
    st.error(f"⚠️ {msg}")
    with st.expander("Technical details"):
        st.code(msg[:1500])


def page_range_picker(container, key):
    """Slider to limit a feature to some pages. Returns None for the whole document."""
    pages = S["pages"]
    if pages < 2:
        return None
    rng = container.slider("Page range", 1, pages, (1, pages), key=key)
    return None if tuple(rng) == (1, pages) else tuple(rng)


def handle_upload(name, data):
    """Index a PDF. Same flow as before: ingest, reset state, remember the file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(data)
        path = f.name
    n = 0
    with st.spinner("Reading and indexing your PDF..."):
        try:
            n = rag.ingest(path)
        except Exception as e:
            st.error(f"Could not read this PDF: {e}")
    if n > 0:
        S.update(fresh_state())
        S.update(loaded=name, chunks=n, pages=rag.page_count, pdf_path=path,
                 size_kb=len(data) / 1024, boot_map=True)
        st.toast("PDF ready!", icon="✅")
        st.rerun()
    elif n == 0:
        st.error("No readable text found. This may be a scanned PDF.")


def use_sample():
    with open(SAMPLE, "rb") as fh:
        S["_sample_bytes"] = fh.read()
    S["_sample_requested"] = True


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown(ui.wordmark(), unsafe_allow_html=True)
    st.markdown(ui.label("Your document"), unsafe_allow_html=True)

    if S["loaded"]:
        st.markdown(ui.doc_card(S["loaded"], S["size_kb"]), unsafe_allow_html=True)
        st.markdown(ui.ring_stats(S["pages"], S["chunks"]), unsafe_allow_html=True)
        with st.expander("Replace document"):
            side_file = st.file_uploader("Upload a PDF", type="pdf", key="side_up", label_visibility="collapsed")
            if side_file and S["loaded"] != side_file.name:
                handle_upload(side_file.name, side_file.getvalue())
    else:
        st.markdown(ui.empty_doc_card(), unsafe_allow_html=True)

    st.markdown(ui.label("Settings"), unsafe_allow_html=True)
    answer_style = st.selectbox("Answer style", list(rag.ANSWER_STYLES.keys()))
    top_k = st.slider("Passages to retrieve", 2, 8, 4,
                      help="How many chunks of the PDF are sent to the AI for each question.")
    st.markdown('<div class="hint">More passages means more context for the model, but a slower answer.</div>',
                unsafe_allow_html=True)

    if S["loaded"]:
        st.markdown(ui.label("How your answer is made"), unsafe_allow_html=True)
        pipe_ph = st.empty()
        pipe_ph.markdown(ui.pipeline(S["pipe"], S["chunks"], top_k), unsafe_allow_html=True)
        st.markdown(ui.label("Your session"), unsafe_allow_html=True)
        st.markdown(ui.session_stats(S["asked"], len(S["quiz_history"])), unsafe_allow_html=True)


# ---------------------------------------------------------------- helpers
def chat_as_text():
    lines = []
    for q, a, p, _ in reversed(S["history"]):
        lines.append(f"Q: {q}\nA: {a}\nPages: {p}\n")
    return "\n".join(lines)


def compute_score(quiz, answers):
    return sum(1 for item, a in zip(quiz, answers) if a == item["answer"])


@st.cache_data(show_spinner=False)
def render_page(path, page_no):
    doc = fitz.open(path)
    pix = doc[page_no - 1].get_pixmap(matrix=fitz.Matrix(1.6, 1.6))
    return pix.tobytes("png")


def render_exchange(q, ans, pages, sources):
    st.markdown(ui.question_block(q), unsafe_allow_html=True)
    st.markdown(ui.answer_md(ans), unsafe_allow_html=True)
    st.markdown(ui.source_chips(pages), unsafe_allow_html=True)
    with st.expander("View source passages"):
        st.markdown(ui.source_cards(sources), unsafe_allow_html=True)


# ================================================================ EMPTY STATE
if not S["loaded"]:
    left, right = st.columns([1.1, 1], gap="large")
    with left:
        st.markdown(ui.empty_headline(), unsafe_allow_html=True)
    with right:
        st.markdown(ui.drop_copy(), unsafe_allow_html=True)
        with st.container(key="main_drop"):
            main_file = st.file_uploader("Upload a PDF", type="pdf", key="main_up", label_visibility="collapsed")
        if os.path.exists(SAMPLE):
            st.button("Try sample.pdf", on_click=use_sample, type="primary", use_container_width=True)
    st.markdown(ui.feature_cards(), unsafe_allow_html=True)

    if main_file and S["loaded"] != main_file.name:
        handle_upload(main_file.name, main_file.getvalue())
    if S.pop("_sample_requested", False):
        handle_upload(SAMPLE, S.pop("_sample_bytes"))
    st.markdown(ui.footer(), unsafe_allow_html=True)
    st.stop()


# ================================================================ HERO + DOCUMENT MAP
status = (f"{len(S['hits'])} passages retrieved" if S["hits"]
          else "Ask a question to see which pages are used")
st.markdown(ui.hero(status), unsafe_allow_html=True)
map_ph = st.empty()
map_mode = "boot" if S["boot_map"] else "idle"
S["boot_map"] = False
map_ph.markdown(ui.docmap(S["pages"], S["chunks"], S["hits"], map_mode), unsafe_allow_html=True)
st.write("")

tab_ask, tab_sum, tab_quiz, tab_cards, tab_terms, tab_view, tab_prog = st.tabs(
    ["Ask", "Summary", "Quiz", "Flashcards", "Key Terms", "Page Viewer", "Progress"])


# ---------------------------------------------------------------- Ask
def run_ask(q):
    """Visual sequence around the real rag.ask() call. Steps are timed for the eye;
    the retrieved pages that light up are the ones rag.ask() really returned."""
    live = live_ph.container()
    with live:
        st.markdown(ui.question_block(q), unsafe_allow_html=True)
        body = st.empty()

    def pipe(n):
        pipe_ph.markdown(ui.pipeline(n, S["chunks"], top_k), unsafe_allow_html=True)

    body.markdown(ui.thinking("Embedding your question"), unsafe_allow_html=True)
    pipe(0)
    time.sleep(0.6)
    pipe(1)
    body.markdown(ui.thinking(f"Searching {S['chunks']} chunks"), unsafe_allow_html=True)
    map_ph.markdown(ui.docmap(S["pages"], S["chunks"], [], "searching"), unsafe_allow_html=True)
    time.sleep(1.0)
    pipe(2)
    body.markdown(ui.thinking("Retrieving passages and writing the answer"), unsafe_allow_html=True)
    try:
        ans, pages, sources = rag.ask(q, k=top_k, style=answer_style)
    except Exception as e:
        live_ph.empty()
        pipe(S["pipe"])
        map_ph.markdown(ui.docmap(S["pages"], S["chunks"], S["hits"]), unsafe_allow_html=True)
        show_error(e)
        return

    hits = []
    for _, meta in sources:
        try:
            hits.append(int(meta["page"]))
        except (KeyError, TypeError, ValueError):
            pass
    for n in range(1, len(hits) + 1):  # light up the real retrieved chunks, one by one
        map_ph.markdown(ui.docmap(S["pages"], S["chunks"], hits[:n]), unsafe_allow_html=True)
        time.sleep(0.25)
    pipe(3)
    tokens = re.split(r"(\s+)", ans)
    step = 3
    pause = min(0.03, 3.0 / max(1, len(tokens) // step))
    for i in range(step, len(tokens) + step, step):
        body.markdown(ui.answer_md("".join(tokens[:i])), unsafe_allow_html=True)
        time.sleep(pause)

    S["history"].insert(0, (q, ans, pages, sources))
    S["asked"] += 1
    S["hits"] = hits
    S["pipe"] = 4
    st.rerun()


def queue_question(text):
    S["pending_q"] = text


with tab_ask:
    with st.form("ask_form", clear_on_submit=True):
        fc1, fc2 = st.columns([6, 1], vertical_alignment="bottom")
        q = fc1.text_input("Ask anything about your document",
                           placeholder="e.g. What is overfitting?", label_visibility="collapsed")
        asked = fc2.form_submit_button("Ask", type="primary", use_container_width=True)

    b1, b2, b3, _sp = st.columns([1.1, 1, 1.1, 3])
    if b1.button("Suggest questions", use_container_width=True):
        with st.spinner("Thinking of questions..."):
            try:
                S["suggestions"] = rag.suggest_questions(5)
            except Exception as e:
                show_error(e)
    if S["history"]:
        if b2.button("Clear chat", use_container_width=True):
            S["history"] = []
            S["hits"] = []
            S["pipe"] = -1
            st.rerun()
        b3.download_button("Download chat", chat_as_text(), file_name="studysense_chat.txt",
                           use_container_width=True)

    if S["suggestions"]:
        with st.container(key="sugg"):
            for idx, sq in enumerate(S["suggestions"]):
                st.button(sq, key=f"sq{idx}", on_click=queue_question, args=(sq,))

    live_ph = st.empty()
    for q_, ans_, pages_, sources_ in S["history"]:
        render_exchange(q_, ans_, pages_, sources_)

    pending = S.pop("pending_q", None)
    if asked and q.strip():
        run_ask(q.strip())
    elif pending:
        run_ask(pending)


# ---------------------------------------------------------------- Summary
with tab_sum:
    s1, s2, s3 = st.columns([1, 1, 1], vertical_alignment="bottom")
    sum_style = s1.selectbox("Summary style", list(rag.SUMMARY_STYLES.keys()))
    sum_range = page_range_picker(s2, "sum_range")
    if s3.button("Generate summary", type="primary"):
        with st.spinner("Summarizing..."):
            try:
                S["summary"] = rag.summarize(sum_style, sum_range)
            except Exception as e:
                show_error(e)
    if S["summary"]:
        with st.container(border=True):
            st.markdown(ui.answer_md(S["summary"]), unsafe_allow_html=True)
        st.download_button("Download summary", S["summary"], file_name="summary.txt")


# ---------------------------------------------------------------- Quiz
with tab_quiz:
    qc1, qc2, qc3, qc4 = st.columns([1, 1, 1, 1], vertical_alignment="bottom")
    n_q = qc1.slider("Number of questions", 3, 10, 5)
    difficulty = qc2.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1)
    quiz_range = page_range_picker(qc3, "quiz_range")
    if qc4.button("Generate new quiz", type="primary"):
        with st.spinner("Creating questions..."):
            try:
                S["quiz"] = rag.generate_quiz(n_q, difficulty, quiz_range)
                S["quiz_id"] += 1
                S["result"] = None
                S["quiz_level"] = difficulty
            except Exception as e:
                show_error(e)

    quiz = S["quiz"]
    if quiz:
        qid = S["quiz_id"]
        with st.form(f"quiz_form_{qid}", border=False):
            answers = []
            for i, item in enumerate(quiz):
                with st.container(border=True):
                    st.markdown(ui.quiz_head(i, item), unsafe_allow_html=True)
                    answers.append(st.radio("Choose one", item["options"], key=f"q{qid}_{i}",
                                            index=None, label_visibility="collapsed"))
            submitted = st.form_submit_button("Submit answers", type="primary")
        if submitted:
            S["result"] = answers
            score = compute_score(quiz, answers)
            S["quiz_history"].append({
                "Quiz": len(S["quiz_history"]) + 1, "Score": score, "Total": len(quiz),
                "Score %": round(100 * score / len(quiz)),
                "Difficulty": S.get("quiz_level", difficulty),
            })
            if score == len(quiz):
                st.balloons()
        if S["result"] is not None:
            result = S["result"]
            st.markdown(ui.quiz_result(compute_score(quiz, result), len(quiz), quiz, result),
                        unsafe_allow_html=True)
    else:
        st.markdown('<div class="hint" style="margin-top:12px">Choose a difficulty and generate a quiz from your document.</div>',
                    unsafe_allow_html=True)


# ---------------------------------------------------------------- Flashcards
with tab_cards:
    f1, f2, f3 = st.columns([1, 1, 1], vertical_alignment="bottom")
    n_cards = f1.slider("Number of flashcards", 4, 15, 8)
    card_range = page_range_picker(f2, "card_range")
    if f3.button("Generate flashcards", type="primary"):
        with st.spinner("Making flashcards..."):
            try:
                S["cards"] = rag.generate_flashcards(n_cards, card_range)
            except Exception as e:
                show_error(e)
    if S["cards"]:
        st.write("")
        components.html(ui.flashcards_html(S["cards"]), height=400)


# ---------------------------------------------------------------- Key terms
with tab_terms:
    t1, t2 = st.columns([1, 1], vertical_alignment="bottom")
    n_terms = t1.slider("Number of terms", 5, 20, 10)
    if t2.button("Extract key terms", type="primary"):
        with st.spinner("Finding key terms..."):
            try:
                S["terms"] = rag.key_terms(n_terms)
            except Exception as e:
                show_error(e)
    terms = S["terms"]
    if terms:
        search = st.text_input("Search terms", placeholder="type to filter...").lower()
        shown = [t for t in terms if search in t["term"].lower() or search in t["definition"].lower()]
        st.markdown(ui.term_cards(shown), unsafe_allow_html=True)
        glossary = "\n".join(f"{t['term']} (Page {t['page']}): {t['definition']}" for t in terms)
        st.download_button("Download glossary", glossary, file_name="glossary.txt")


# ---------------------------------------------------------------- Page viewer
with tab_view:
    st.caption("Check any page of your PDF, for example to verify the sources the AI cited.")
    total = S["pages"]
    vleft, vright = st.columns([1.3, 1], gap="large")
    with vright:
        page_no = st.number_input("Page number", min_value=1, max_value=max(total, 1), value=1, step=1)
        ranks = [i + 1 for i, p in enumerate(S["hits"]) if p == int(page_no)]
        st.markdown(ui.page_info(int(page_no), ranks), unsafe_allow_html=True)
    with vleft:
        try:
            st.image(render_page(S["pdf_path"], int(page_no)), use_container_width=True)
        except Exception as e:
            st.error(f"Could not display this page: {e}")


# ---------------------------------------------------------------- Progress
with tab_prog:
    hist = S["quiz_history"]
    if hist:
        avg = f"{sum(h['Score %'] for h in hist) / len(hist):.0f}%"
        best = f"{max(h['Score %'] for h in hist)}%"
    else:
        avg = best = "-"
    st.markdown(ui.metrics(S["asked"], len(hist), avg, best), unsafe_allow_html=True)
    if hist:
        st.markdown(ui.bar_chart([h["Score %"] for h in hist]), unsafe_allow_html=True)
        with st.expander("Quiz history"):
            st.dataframe(pd.DataFrame(hist), hide_index=True, use_container_width=True)
    else:
        st.markdown('<div class="hint" style="margin-top:14px">Take a quiz and your scores will appear here.</div>',
                    unsafe_allow_html=True)

st.markdown(ui.footer(), unsafe_allow_html=True)