import html
import tempfile

import fitz  # PyMuPDF
import pandas as pd
import streamlit as st

import rag

st.set_page_config(page_title="StudySense", page_icon="📚", layout="wide")

# ---------------------------------------------------------------- styling
st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
    padding: 2rem 2.5rem; border-radius: 18px; color: white; margin-bottom: 1.2rem;
}
.hero h1 { margin: 0; font-size: 2.6rem; color: white; }
.hero p { margin: 0.4rem 0 0 0; font-size: 1.1rem; opacity: 0.92; }
.chip {
    display: inline-block; background: #4f46e5; color: white;
    padding: 3px 12px; border-radius: 999px; font-size: 0.85rem; margin-right: 6px;
}
.source-card {
    background: #f9fafb; color: #374151; border: 1px solid #e5e7eb;
    padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 0.5rem; font-size: 0.92rem;
}
.flashcard {
    background: linear-gradient(135deg, #eef2ff, #fae8ff); color: #1f2937;
    border: 2px solid #c4b5fd; border-radius: 16px; padding: 2.2rem 1.5rem;
    text-align: center; font-size: 1.35rem; min-height: 150px; margin-bottom: 0.8rem;
}
.flashcard.back {
    background: linear-gradient(135deg, #ecfdf5, #d1fae5); border-color: #6ee7b7;
}
.term-card {
    background: #f5f3ff; color: #1f2937; border-left: 6px solid #7c3aed;
    padding: 0.8rem 1.1rem; border-radius: 10px; margin-bottom: 0.6rem;
}
.feature-card {
    border: 1px solid #c4b5fd; border-radius: 14px; padding: 1rem 1.2rem; height: 100%;
}
.footer { text-align: center; color: #9ca3af; margin-top: 3rem; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>📚 StudySense</h1>
  <p>Your AI study partner. Upload a PDF, ask questions with page references,
  get summaries, quizzes, flashcards and key terms.</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------- state
def fresh_state():
    return {
        "loaded": None, "chunks": 0, "pages": 0, "pdf_path": None,
        "history": [], "asked": 0, "suggestions": [],
        "summary": None,
        "quiz": [], "quiz_id": 0, "result": None, "quiz_history": [],
        "cards": [], "card_i": 0, "show_back": False,
        "terms": [],
    }


for key, value in fresh_state().items():
    st.session_state.setdefault(key, value)


def page_range_picker(container, key):
    """Slider to limit a feature to some pages. Returns None for the whole document."""
    pages = st.session_state["pages"]
    if pages < 2:
        return None
    rng = container.slider("Page range", 1, pages, (1, pages), key=key)
    return None if tuple(rng) == (1, pages) else tuple(rng)


def show_error(e):
    msg = str(e)
    st.error(f"⚠️ {msg}")
    with st.expander("Technical details"):
        st.code(msg[:1500])


def esc(text):
    return html.escape(str(text))


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.header("📄 Your Document")
    file = st.file_uploader("Upload a PDF", type="pdf")

    if file and st.session_state["loaded"] != file.name:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(file.getvalue())
            path = f.name
        n = 0
        with st.spinner("Reading and indexing your PDF..."):
            try:
                n = rag.ingest(path)
            except Exception as e:
                st.error(f"Could not read this PDF: {e}")
        if n > 0:
            st.session_state.update(fresh_state())
            st.session_state.update(loaded=file.name, chunks=n,
                                    pages=rag.page_count, pdf_path=path)
            st.toast("PDF ready!", icon="✅")
        elif n == 0:
            st.error("No readable text found. This may be a scanned PDF.")

    if st.session_state["loaded"]:
        st.markdown(f"**File:** {st.session_state['loaded']}")
        c1, c2 = st.columns(2)
        c1.metric("Pages", st.session_state["pages"])
        c2.metric("Chunks", st.session_state["chunks"])

    st.divider()
    st.subheader("⚙️ Settings")
    answer_style = st.selectbox("Answer style", list(rag.ANSWER_STYLES.keys()))
    top_k = st.slider("Passages to retrieve", 2, 8, 4,
                      help="How many chunks of the PDF are sent to the AI for each question.")

    if st.session_state["loaded"]:
        st.divider()
        st.subheader("📊 Your session")
        s1, s2 = st.columns(2)
        s1.metric("Questions", st.session_state["asked"])
        s2.metric("Quizzes", len(st.session_state["quiz_history"]))

    st.divider()
    st.markdown("**How it works**")
    st.caption("1. PDF is split into chunks\n\n2. Chunks become embeddings\n\n"
               "3. Best chunks are retrieved\n\n4. AI answers using only those chunks")


# ---------------------------------------------------------------- helpers
def answer_question(q):
    with st.spinner("Searching your document..."):
        try:
            ans, pages, sources = rag.ask(q, k=top_k, style=answer_style)
            st.session_state["history"].insert(0, (q, ans, pages, sources))
            st.session_state["asked"] += 1
        except Exception as e:
            show_error(e)


def chat_as_text():
    lines = []
    for q, a, p, _ in reversed(st.session_state["history"]):
        lines.append(f"Q: {q}\nA: {a}\nPages: {p}\n")
    return "\n".join(lines)


def next_card():
    st.session_state["card_i"] = (st.session_state["card_i"] + 1) % len(st.session_state["cards"])
    st.session_state["show_back"] = False


def prev_card():
    st.session_state["card_i"] = (st.session_state["card_i"] - 1) % len(st.session_state["cards"])
    st.session_state["show_back"] = False


def flip_card():
    st.session_state["show_back"] = not st.session_state["show_back"]


def compute_score(quiz, answers):
    return sum(1 for item, a in zip(quiz, answers) if a == item["answer"])


@st.cache_data(show_spinner=False)
def render_page(path, page_no):
    doc = fitz.open(path)
    pix = doc[page_no - 1].get_pixmap(matrix=fitz.Matrix(1.6, 1.6))
    return pix.tobytes("png")


# ---------------------------------------------------------------- main area
if not st.session_state["loaded"]:
    st.info("👈 Upload a PDF from the sidebar to get started.")
    cols = st.columns(5)
    cards = [
        ("💬 Ask", "Get answers with page references."),
        ("📝 Summarize", "Short, detailed or exam-revision style."),
        ("🎯 Quiz", "Choose difficulty and page range, get scored."),
        ("🃏 Flashcards", "Flip cards to memorize key ideas."),
        ("🔑 Key Terms", "A searchable glossary of the document."),
    ]
    for col, (title, desc) in zip(cols, cards):
        col.markdown(f'<div class="feature-card"><b>{title}</b><br>{desc}</div>',
                     unsafe_allow_html=True)
else:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "💬 Ask", "📝 Summary", "🎯 Quiz", "🃏 Flashcards",
        "🔑 Key Terms", "📄 Page Viewer", "📊 Progress"])

    # ============================================================ Ask
    with tab1:
        with st.form("ask_form", clear_on_submit=True):
            q = st.text_input("Ask anything about your document",
                              placeholder="e.g. What is overfitting?")
            asked = st.form_submit_button("Ask 🔍")
        if asked and q.strip():
            answer_question(q.strip())

        bc1, bc2, bc3 = st.columns([1, 1, 1])
        if bc1.button("💡 Suggest questions"):
            with st.spinner("Thinking of questions..."):
                try:
                    st.session_state["suggestions"] = rag.suggest_questions(5)
                except Exception as e:
                    show_error(e)
        if st.session_state["history"]:
            if bc2.button("🗑️ Clear chat"):
                st.session_state["history"] = []
                st.rerun()
            bc3.download_button("⬇️ Download chat", chat_as_text(), file_name="studysense_chat.txt")

        for idx, sq in enumerate(st.session_state["suggestions"]):
            if st.button(f"❓ {sq}", key=f"sq{idx}"):
                answer_question(sq)

        for q_, ans_, pages_, sources_ in st.session_state["history"]:
            with st.chat_message("user"):
                st.write(q_)
            with st.chat_message("assistant"):
                st.markdown(ans_)
                chips = "".join(f'<span class="chip">Page {p}</span>' for p in pages_)
                st.markdown("**Sources:** " + chips, unsafe_allow_html=True)
                with st.expander("📖 View source passages"):
                    for text, meta in sources_:
                        st.markdown(
                            f'<div class="source-card"><b>Page {meta["page"]}</b><br>{esc(text)}</div>',
                            unsafe_allow_html=True)

    # ============================================================ Summary
    with tab2:
        s1, s2 = st.columns(2)
        sum_style = s1.selectbox("Summary style", list(rag.SUMMARY_STYLES.keys()))
        sum_range = page_range_picker(s2, "sum_range")
        if st.button("✨ Generate Summary"):
            with st.spinner("Summarizing..."):
                try:
                    st.session_state["summary"] = rag.summarize(sum_style, sum_range)
                except Exception as e:
                    show_error(e)
        if st.session_state["summary"]:
            st.markdown(st.session_state["summary"])
            st.download_button("⬇️ Download summary", st.session_state["summary"],
                               file_name="summary.txt")

    # ============================================================ Quiz
    with tab3:
        qc1, qc2, qc3 = st.columns(3)
        n_q = qc1.slider("Number of questions", 3, 10, 5)
        difficulty = qc2.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1)
        quiz_range = page_range_picker(qc3, "quiz_range")

        if st.button("🎲 Generate New Quiz"):
            with st.spinner("Creating questions..."):
                try:
                    st.session_state["quiz"] = rag.generate_quiz(n_q, difficulty, quiz_range)
                    st.session_state["quiz_id"] += 1
                    st.session_state["result"] = None
                    st.session_state["quiz_level"] = difficulty
                except Exception as e:
                    show_error(e)

        quiz = st.session_state["quiz"]
        if quiz:
            qid = st.session_state["quiz_id"]
            with st.form(f"quiz_form_{qid}"):
                answers = []
                for i, item in enumerate(quiz):
                    st.markdown(f"**Q{i+1}. {item['question']}**")
                    answers.append(st.radio("Choose one", item["options"],
                                            key=f"q{qid}_{i}", index=None,
                                            label_visibility="collapsed"))
                    st.write("")
                submitted = st.form_submit_button("Submit Answers ✅")

            if submitted:
                st.session_state["result"] = answers
                score = compute_score(quiz, answers)
                st.session_state["quiz_history"].append({
                    "Quiz": len(st.session_state["quiz_history"]) + 1,
                    "Score": score, "Total": len(quiz),
                    "Score %": round(100 * score / len(quiz)),
                    "Difficulty": st.session_state.get("quiz_level", difficulty),
                })
                if score == len(quiz):
                    st.balloons()

            if st.session_state["result"] is not None:
                result = st.session_state["result"]
                score = compute_score(quiz, result)
                st.markdown(f"## 🏆 Score: {score} / {len(quiz)}")
                st.progress(score / len(quiz))
                for i, item in enumerate(quiz):
                    chosen = result[i]
                    if chosen == item["answer"]:
                        st.success(f"Q{i+1}: Correct ✅ (Page {item['page']})")
                    else:
                        shown = chosen if chosen else "Not answered"
                        st.error(f"Q{i+1}: Wrong ❌ You chose: {shown}\n\n"
                                 f"Correct answer: {item['answer']} (Page {item['page']})")
                    if item["explanation"]:
                        st.caption(f"💡 {item['explanation']}")

    # ============================================================ Flashcards
    with tab4:
        f1, f2 = st.columns(2)
        n_cards = f1.slider("Number of flashcards", 4, 15, 8)
        card_range = page_range_picker(f2, "card_range")
        if st.button("🃏 Generate Flashcards"):
            with st.spinner("Making flashcards..."):
                try:
                    st.session_state["cards"] = rag.generate_flashcards(n_cards, card_range)
                    st.session_state["card_i"] = 0
                    st.session_state["show_back"] = False
                except Exception as e:
                    show_error(e)

        cards = st.session_state["cards"]
        if cards:
            i = st.session_state["card_i"]
            card = cards[i]
            st.caption(f"Card {i + 1} of {len(cards)}  ·  Page {card['page']}")
            if st.session_state["show_back"]:
                st.markdown(f'<div class="flashcard back">{esc(card["back"])}</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="flashcard"><b>{esc(card["front"])}</b></div>',
                            unsafe_allow_html=True)
            b1, b2, b3 = st.columns(3)
            b1.button("⬅️ Previous", on_click=prev_card, use_container_width=True)
            b2.button("🔄 Flip card", on_click=flip_card, use_container_width=True)
            b3.button("Next ➡️", on_click=next_card, use_container_width=True)

    # ============================================================ Key terms
    with tab5:
        n_terms = st.slider("Number of terms", 5, 20, 10)
        if st.button("🔑 Extract Key Terms"):
            with st.spinner("Finding key terms..."):
                try:
                    st.session_state["terms"] = rag.key_terms(n_terms)
                except Exception as e:
                    show_error(e)

        terms = st.session_state["terms"]
        if terms:
            search = st.text_input("🔎 Search terms", placeholder="type to filter...")
            shown = [t for t in terms
                     if search.lower() in t["term"].lower() or search.lower() in t["definition"].lower()]
            for t in shown:
                st.markdown(
                    f'<div class="term-card"><b>{esc(t["term"])}</b> '
                    f'<span class="chip">Page {esc(t["page"])}</span><br>{esc(t["definition"])}</div>',
                    unsafe_allow_html=True)
            glossary = "\n".join(f"{t['term']} (Page {t['page']}): {t['definition']}" for t in terms)
            st.download_button("⬇️ Download glossary", glossary, file_name="glossary.txt")

    # ============================================================ Page viewer
    with tab6:
        st.caption("Check any page of your PDF, for example to verify the sources the AI cited.")
        total = st.session_state["pages"]
        page_no = st.number_input("Page number", min_value=1, max_value=max(total, 1), value=1, step=1)
        try:
            st.image(render_page(st.session_state["pdf_path"], int(page_no)), width=650)
        except Exception as e:
            st.error(f"Could not display this page: {e}")

    # ============================================================ Progress
    with tab7:
        hist = st.session_state["quiz_history"]
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Questions asked", st.session_state["asked"])
        m2.metric("Quizzes taken", len(hist))
        if hist:
            avg = sum(h["Score %"] for h in hist) / len(hist)
            m3.metric("Average score", f"{avg:.0f}%")
            m4.metric("Best score", f"{max(h['Score %'] for h in hist)}%")
            df = pd.DataFrame(hist)
            st.markdown("#### Quiz scores")
            st.bar_chart(df.set_index("Quiz")["Score %"])
            st.dataframe(df, hide_index=True)
        else:
            m3.metric("Average score", "-")
            m4.metric("Best score", "-")
            st.info("Take a quiz and your scores will appear here.")

st.markdown('<div class="footer">StudySense · Built with RAG, Streamlit and Ollama</div>',
            unsafe_allow_html=True)