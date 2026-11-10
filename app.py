import os
import tempfile
import time

import fitz  # PyMuPDF
import pandas as pd
import streamlit as st

import rag
from components import ui
from styles import inject_styles

st.set_page_config(page_title="StudySense", page_icon="📚", layout="wide")

inject_styles()

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
    st.error(msg)
    with st.expander("Technical details"):
        st.code(msg[:1500])


def file_size(path):
    size = os.path.getsize(path)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024


pipeline_placeholder = None
document_map_placeholder = None


def selected_page():
    try:
        page = int(st.query_params.get("page", "1"))
    except (TypeError, ValueError):
        return 1
    return max(1, min(page, max(st.session_state["pages"], 1)))


def page_chunk_counts():
    counts = {page: 0 for page in range(1, st.session_state["pages"] + 1)}
    for _, page in rag.all_chunks:
        if page in counts:
            counts[page] += 1
    return counts


def render_document_map():
    counts = page_chunk_counts()
    latest_sources = st.session_state["history"][0][3] if st.session_state["history"] else []
    st.markdown(ui.document_map_header(len(latest_sources)), unsafe_allow_html=True)
    if not counts:
        st.markdown(ui.document_map_legend(), unsafe_allow_html=True)
        return

    max_chunks = max(counts.values(), default=0)
    pages = list(counts)
    columns_per_row = min(len(pages), 10)
    for row_start in range(0, len(pages), columns_per_row):
        row_pages = pages[row_start:row_start + columns_per_row]
        columns = st.columns(columns_per_row)
        for column, page in zip(columns, row_pages):
            with column:
                st.markdown(
                    f'<div class="page-map-item page-map-page-{page}" '
                    f'style="--page-index: {page - 1};">'
                    + ui.page_thumbnail(page, counts[page], max_chunks)
                    + '</div>',
                    unsafe_allow_html=True)
                if st.button(f"Open page {page}", key=f"page_map_{page}"):
                    st.query_params["page"] = str(page)
    st.markdown(ui.document_map_legend(), unsafe_allow_html=True)


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown(ui.sidebar_wordmark(), unsafe_allow_html=True)
    st.header("Your Document")
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
        st.markdown(
            ui.document_card(st.session_state["loaded"],
                             file_size(st.session_state["pdf_path"])),
            unsafe_allow_html=True)
        st.markdown(ui.indexing_ring(st.session_state["pages"],
                                     st.session_state["chunks"]),
                    unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="settings-label">SETTINGS</div>',
                unsafe_allow_html=True)
    answer_style = st.selectbox("Answer style", list(rag.ANSWER_STYLES.keys()))
    top_k = st.slider("Passages to retrieve", 2, 8, 4,
                      help="How many chunks of the PDF are sent to the AI for each question.",
                      label_visibility="collapsed")
    st.markdown("Passages to retrieve " + ui.passages_pill(top_k),
                unsafe_allow_html=True)
    st.markdown(
        '<div class="settings-hint">More passages means more context.</div>',
        unsafe_allow_html=True)

    if st.session_state["loaded"]:
        pipeline_placeholder = st.empty()
        document_map_placeholder = st.empty()
        pipeline_placeholder.markdown(ui.pipeline(), unsafe_allow_html=True)
        document_map_placeholder.markdown(
            ui.document_map(st.session_state["chunks"]),
            unsafe_allow_html=True)
        st.divider()
        st.markdown('<div class="settings-label">YOUR SESSION</div>',
                    unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        s1.metric("Questions", st.session_state["asked"])
        s2.metric("Quizzes", len(st.session_state["quiz_history"]))

# ---------------------------------------------------------------- document map
if st.session_state["loaded"]:
    render_document_map()
else:
    st.markdown(ui.document_map_header(0), unsafe_allow_html=True)

# ---------------------------------------------------------------- helpers
def render_ask_pipeline(stage, sources=None):
    if pipeline_placeholder is None or document_map_placeholder is None:
        return

    retrieved_indices = {}
    if sources:
        used = set()
        for rank, (text, meta) in enumerate(sources, start=1):
            for index, (chunk, page) in enumerate(rag.all_chunks):
                if index not in used and chunk == text and page == meta.get("page"):
                    retrieved_indices[index] = rank
                    used.add(index)
                    break
    pipeline_placeholder.markdown(
        ui.pipeline(stage, len(sources) if sources else 0),
        unsafe_allow_html=True)
    document_map_placeholder.markdown(
        ui.document_map(st.session_state["chunks"], retrieved_indices, stage),
        unsafe_allow_html=True)


def answer_question(q):
    try:
        render_ask_pipeline("embed")
        time.sleep(0.18)
        render_ask_pipeline("search")
        ans, pages, sources = rag.ask(q, k=top_k, style=answer_style)
        render_ask_pipeline("retrieve", sources)
        time.sleep(min(0.9, max(0.25, len(sources) * 0.14)))
        render_ask_pipeline("write", sources)
        time.sleep(0.45)
        st.session_state["history"].insert(0, (q, ans, pages, sources))
        st.session_state["asked"] += 1
        render_ask_pipeline("done", sources)
    except Exception as e:
        render_ask_pipeline("idle")
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
        ("Ask", "Get answers with page references."),
        ("Summarize", "Short, detailed or exam-revision style."),
        ("Quiz", "Choose difficulty and page range, get scored."),
        ("Flashcards", "Flip cards to memorize key ideas."),
        ("Key Terms", "A searchable glossary of the document."),
    ]
    for col, (title, desc) in zip(cols, cards):
        col.markdown(ui.feature_card(title, desc), unsafe_allow_html=True)
else:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Ask", "Summary", "Quiz", "Flashcards",
        "Key Terms", "Page Viewer", "Progress"])

    # ============================================================ Ask
    with tab1:
        with st.form("ask_form", clear_on_submit=True):
            ask_col, ask_button_col = st.columns([5, 1])
            q = ask_col.text_input("Ask anything about your document",
                                   placeholder="e.g. What is overfitting?",
                                   label_visibility="collapsed")
            asked = ask_button_col.form_submit_button("Ask")
        if asked and q.strip():
            answer_question(q.strip())

        bc1, bc2, bc3 = st.columns([1, 1, 1])
        if bc1.button("Suggest questions", use_container_width=True):
            with st.spinner("Thinking of questions..."):
                try:
                    st.session_state["suggestions"] = rag.suggest_questions(5)
                except Exception as e:
                    show_error(e)
        if bc2.button("Clear chat", use_container_width=True) and st.session_state["history"]:
            st.session_state["history"] = []
            st.rerun()
        if st.session_state["history"]:
            bc3.download_button("Download chat", chat_as_text(),
                                file_name="studysense_chat.txt",
                                use_container_width=True)
        else:
            bc3.button("Download chat", disabled=True, use_container_width=True)

        if st.session_state["suggestions"]:
            st.markdown('<div class="suggestions-anchor"></div>', unsafe_allow_html=True)
        for idx, sq in enumerate(st.session_state["suggestions"]):
            if st.button(sq, key=f"sq{idx}"):
                answer_question(sq)

        for q_, ans_, pages_, sources_ in st.session_state["history"]:
            st.markdown(ui.exchange(q_, ans_, pages_, sources_), unsafe_allow_html=True)
            with st.expander("View source passages"):
                for rank, (text, meta) in enumerate(sources_, start=1):
                    st.markdown(ui.source_passage(text, meta["page"], rank, len(sources_)),
                                unsafe_allow_html=True)

    # ============================================================ Summary
    with tab2:
        s1, s2 = st.columns(2)
        sum_style = s1.selectbox("Summary style", list(rag.SUMMARY_STYLES.keys()))
        sum_range = page_range_picker(s2, "sum_range")
        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                try:
                    st.session_state["summary"] = rag.summarize(sum_style, sum_range)
                except Exception as e:
                    show_error(e)
        if st.session_state["summary"]:
            st.markdown(st.session_state["summary"])
            st.download_button("Download summary", st.session_state["summary"],
                               file_name="summary.txt")

    # ============================================================ Quiz
    with tab3:
        qc1, qc2, qc3 = st.columns(3)
        n_q = qc1.slider("Number of questions", 3, 10, 5)
        difficulty = qc2.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1)
        quiz_range = page_range_picker(qc3, "quiz_range")

        if st.button("Generate New Quiz"):
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
            current_answers = [
                st.session_state.get(f"q{qid}_{i}") for i in range(len(quiz))
            ]
            st.markdown(ui.quiz_progress(quiz, current_answers), unsafe_allow_html=True)
            with st.form(f"quiz_form_{qid}"):
                answers = []
                for i, item in enumerate(quiz):
                    st.markdown(
                        f'<div class="quiz-card"><div class="quiz-number">QUESTION {i + 1}</div>'
                        f'<h3>{ui.esc(item["question"])}</h3>',
                        unsafe_allow_html=True)
                    answers.append(st.radio("Choose one", item["options"],
                                            key=f"q{qid}_{i}", index=None,
                                            label_visibility="collapsed"))
                    st.markdown("</div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Submit Answers")

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
                st.markdown('<div class="quiz-result">', unsafe_allow_html=True)
                st.markdown(ui.quiz_score_ring(score, len(quiz)), unsafe_allow_html=True)
                st.markdown(f"## Score: {score} / {len(quiz)}")
                for i, item in enumerate(quiz):
                    chosen = result[i]
                    st.markdown(ui.quiz_option_review(item, chosen),
                                unsafe_allow_html=True)
                    if chosen == item["answer"]:
                        st.markdown(
                            f'<div class="quiz-feedback correct"><b>Q{i + 1}: Correct</b>'
                            f'<span>Page {ui.esc(item["page"])}</span></div>',
                            unsafe_allow_html=True)
                    else:
                        shown = chosen if chosen else "Not answered"
                        st.markdown(
                            f'<div class="quiz-feedback wrong"><b>Q{i + 1}: Wrong</b>'
                            f'<span>You chose: {ui.esc(shown)} · Correct: '
                            f'{ui.esc(item["answer"])} · Page {ui.esc(item["page"])}</span></div>',
                            unsafe_allow_html=True)
                    if item["explanation"]:
                        st.markdown(
                            f'<div class="quiz-explanation">{ui.esc(item["explanation"])}</div>',
                            unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================ Flashcards
    with tab4:
        f1, f2 = st.columns(2)
        n_cards = f1.slider("Number of flashcards", 4, 15, 8)
        card_range = page_range_picker(f2, "card_range")
        if st.button("Generate Flashcards"):
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
            st.markdown(
                f'<div class="deck-meta">Card {i + 1} of {len(cards)} · Page {card["page"]}</div>',
                unsafe_allow_html=True)
            st.markdown(
                f'<div class="deck-progress"><span style="width: '
                f'{100 * (i + 1) / len(cards):.1f}%"></span></div>',
                unsafe_allow_html=True)
            st.markdown(ui.flashcard_surface(card["front"], card["back"],
                                             st.session_state["show_back"]),
                        unsafe_allow_html=True)
            b1, b2, b3 = st.columns(3)
            b1.button("Previous", on_click=prev_card, use_container_width=True)
            b2.button("Flip card", on_click=flip_card, use_container_width=True)
            b3.button("Next", on_click=next_card, use_container_width=True)

    # ============================================================ Key terms
    with tab5:
        n_terms = st.slider("Number of terms", 5, 20, 10)
        if st.button("Extract Key Terms"):
            with st.spinner("Finding key terms..."):
                try:
                    st.session_state["terms"] = rag.key_terms(n_terms)
                except Exception as e:
                    show_error(e)

        terms = st.session_state["terms"]
        if terms:
            search = st.text_input("Search terms", placeholder="type to filter...")
            shown = [t for t in terms
                     if search.lower() in t["term"].lower() or search.lower() in t["definition"].lower()]
            st.markdown(ui.terms_grid_start(), unsafe_allow_html=True)
            term_columns = st.columns(3)
            for index, t in enumerate(shown):
                with term_columns[index % 3]:
                    st.markdown(ui.term_card(t["term"], t["page"], t["definition"]),
                                unsafe_allow_html=True)
            st.markdown(ui.terms_grid_end(), unsafe_allow_html=True)
            glossary = "\n".join(f"{t['term']} (Page {t['page']}): {t['definition']}" for t in terms)
            st.download_button("Download glossary", glossary, file_name="glossary.txt")

    # ============================================================ Page viewer
    with tab6:
        st.caption("Check any page of your PDF, for example to verify the sources the AI cited.")
        total = st.session_state["pages"]
        page_no = st.number_input("Page number", min_value=1, max_value=max(total, 1),
                                  value=selected_page(), step=1)
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

st.markdown(ui.footer(), unsafe_allow_html=True)