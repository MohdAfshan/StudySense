import html
import re

from styles import FLASHCARD_IFRAME_CSS

def esc(text):
    return html.escape(str(text))


def document_map_header(retrieved_count):
    status = (
        f'<div class="map-status"><span class="status-dot"></span>'
        f'{int(retrieved_count)} passages retrieved</div>'
    )
    return (
        '<div class="map-heading"><div><h1 class="map-wordmark">'
        '<span>Study</span><span>Sense</span></h1>'
        '<p>Turn your documents into understanding.</p></div>'
        + status + '</div>'
    )


def page_thumbnail(page_number, chunk_count, max_chunks):
    density = chunk_count / max_chunks if max_chunks else 0
    first_width = 42 + round(density * 34)
    second_width = 28 + round(density * 42)
    return (
        f'<div class="page-thumbnail" style="--page-density: {density:.2f};">'
        f'<div class="page-fold"></div><div class="page-lines">'
        f'<span style="width: {first_width}%"></span>'
        f'<span style="width: {second_width}%"></span></div>'
        f'<div class="page-number">{int(page_number)}</div></div>'
    )


def document_map_legend():
    return (
        '<div class="map-legend"><span><i class="legend-swatch"></i>'
        'Indexed page</span><span><i class="legend-swatch legend-dense"></i>'
        'Relative chunk density</span></div>'
    )


def feature_card(title, description):
    return f'<div class="feature-card"><b>{esc(title)}</b><br>{esc(description)}</div>'


def source_chips(pages):
    return "".join(
        f'<span class="chip source-chip source-page-{esc(page)}" '
        f'data-page="{esc(page)}">Page {esc(page)}</span>' for page in pages
    )


def answer_text(answer):
    return re.sub(
        r"\(Page\s+(\d+)\)",
        r'<span class="page-reference">Page \1</span>',
        str(answer),
        flags=re.IGNORECASE,
    )


def source_passage(text, page, rank, total):
    strength = max(28, round(100 - ((rank - 1) / max(total, 1)) * 55))
    return (
        f'<div class="source-passage source-page-{esc(page)}">'
        f'<div class="source-passage-meta"><span>Page {esc(page)}</span>'
        f'<span>Rank {int(rank)}</span></div>'
        f'<div class="similarity-track"><span style="width: {strength}%"></span></div>'
        f'<div class="source-passage-text">{esc(text)}</div></div>'
    )


def quiz_progress(quiz, answers):
    segments = []
    for index in range(len(quiz)):
        state = "filled" if index < len(answers) and answers[index] is not None else ""
        segments.append(f'<span class="quiz-segment {state}"></span>')
    return '<div class="quiz-progress">' + "".join(segments) + "</div>"


def quiz_score_ring(score, total):
    percent = round(100 * score / total) if total else 0
    return (
        f'<div class="score-ring" style="--score: {percent * 3.6}deg;">'
        f'<div><strong>{percent}%</strong><span>Score</span></div></div>'
    )


def quiz_option_review(item, chosen):
    rows = []
    for index, option in enumerate(item["options"]):
        state = "correct-option" if option == item["answer"] else ""
        if chosen == option and option != item["answer"]:
            state = "wrong-option"
        rows.append(
            f'<div class="quiz-option-review {state}">'
            f'<span>{chr(65 + index)}</span>{esc(option)}</div>'
        )
    return "".join(rows)


def flashcard_surface(front, back, show_back):
    front_text = esc(front)
    back_text = esc(back)
    flipped = " flipped" if show_back else ""
    return (
        f'<div class="flashcard-scene"><div class="flashcard-3d{flipped}">'
        f'<div class="flashcard-face flashcard-front"><span>{front_text}</span></div>'
        f'<div class="flashcard-face flashcard-back"><span>{back_text}</span></div>'
        '</div></div>'
    )


def flashcard_iframe(front, back, show_back):
    initial = "flipped" if show_back else ""
    return f"""<style>{FLASHCARD_IFRAME_CSS}</style>
    <div class="scene" onclick="this.firstElementChild.classList.toggle('flipped')">
      <div class="card {initial}">
        <div class="face front">{esc(front)}</div>
        <div class="face back">{esc(back)}</div>
      </div>
    </div>
    """


def exchange(question, answer, pages, sources):
    return (
        '<article class="ask-exchange">'
        '<div class="question-label">YOU</div>'
        f'<h3 class="ask-question">{esc(question)}</h3>'
        f'<div class="ask-answer answer-fade">{answer_text(answer)}</div>'
        f'<div class="ask-sources"><span class="sources-label">SOURCES</span>'
        f'{source_chips(pages)}</div>'
        '</article>'
    )


def flashcard(text, back=False):
    card_class = "flashcard back" if back else "flashcard"
    content = esc(text) if back else f"<b>{esc(text)}</b>"
    return f'<div class="{card_class}">{content}</div>'


def term_card(term, page, definition):
    return (
        f'<div class="term-card"><b>{esc(term)}</b> '
        f'<span class="chip page-label">Page {esc(page)}</span><br>'
        f'{esc(definition)}</div>'
    )


def terms_grid_start():
    return '<div class="terms-grid">'


def terms_grid_end():
    return "</div>"


def progress_metric(label, value, suffix=""):
    if isinstance(value, int):
        value_markup = (
            f'<strong class="metric-number" style="--metric-target: {value};">'
            f'<span>{suffix}</span></strong>'
        )
    else:
        value_markup = f'<strong class="metric-static">{esc(value)}</strong>'
    return (
        f'<div class="progress-metric"><span class="progress-metric-label">{esc(label)}</span>'
        f'{value_markup}</div>'
    )


def quiz_chart(history):
    if not history:
        return ""
    bars = []
    for index, item in enumerate(history):
        score = max(0, min(100, int(item["Score %"])))
        bars.append(
            f'<div class="chart-column" style="--bar-height: {score}%; '
            f'--bar-index: {index};"><span class="chart-value">{score}%</span>'
            f'<div class="chart-bar"></div><span class="chart-label">Quiz {item["Quiz"]}</span></div>'
        )
    return (
        '<div class="quiz-chart"><div class="chart-y-axis">'
        '<span>100</span><span>75</span><span>50</span><span>25</span><span>0</span>'
        '</div><div class="chart-plot"><div class="chart-grid"></div>'
        '<div class="chart-bars">' + "".join(bars) + "</div></div></div>"
    )


def footer():
    return '<div class="footer">StudySense · Built with RAG, Streamlit and Ollama</div>'


def sidebar_wordmark():
    return (
        '<div class="sidebar-wordmark" aria-label="StudySense">'
        '<span>Study</span><span class="wordmark-sense">Sense</span>'
        '</div>'
    )


def document_card(file_name, file_size):
    return (
        '<div class="document-card">'
        '<div class="pdf-icon">PDF</div>'
        '<div class="document-details">'
        f'<strong>{esc(file_name)}</strong>'
        f'<span>{esc(file_size)}</span>'
        '</div></div>'
    )


def indexing_ring(pages, chunks):
    return (
        f'<div class="indexing-summary" style="--target-pages: {int(pages)}; '
        f'--target-chunks: {int(chunks)};">'
        '<div class="progress-ring" style="--ring-progress: 100%; '
        f'--target-pages: {int(pages)}; --target-chunks: {int(chunks)};">'
        '<span class="ring-check">OK</span></div>'
        '<div class="indexing-counts">'
        '<div><strong class="count-pages"></strong><span>Pages</span></div>'
        '<div><strong class="count-chunks"></strong><span>Chunks</span></div>'
        '</div></div>'
    )


def passages_pill(value):
    return f'<span class="value-pill">{int(value)}</span>'


def document_map(chunk_count, retrieved_indices=None, stage="idle"):
    retrieved_indices = retrieved_indices or {}
    chunks = []
    for index in range(chunk_count):
        rank = retrieved_indices.get(index)
        classes = ["document-chunk"]
        if stage == "search":
            classes.append("chunk-searching")
        if rank is not None:
            classes.append("chunk-retrieved")
        delay_ms = rank * 140 if rank is not None else index * 18
        delay = f"animation-delay: {delay_ms}ms;"
        label = f"<span>{rank}</span>" if rank is not None else ""
        chunks.append(
            f'<span class="{" ".join(classes)}" style="{delay}">{label}</span>'
        )
    return (
        '<div class="document-map-wrap">'
        '<div class="pipeline-label">DOCUMENT MAP</div>'
        '<div class="document-map">' + "".join(chunks) + '</div>'
        '</div>'
    )


def pipeline(stage="idle", retrieved_count=0):
    steps = [
        ("embed", "Embed the question"),
        ("search", "Search the chunks"),
        ("retrieve", "Retrieve the best passages"),
        ("write", "Write the answer"),
    ]
    active_index = next((i for i, (key, _) in enumerate(steps) if key == stage), -1)
    if stage == "done":
        active_index = len(steps)
    items = []
    for index, (key, label) in enumerate(steps):
        state = "complete" if index < active_index else "active" if index == active_index else ""
        marker = "OK" if state == "complete" else str(index + 1)
        items.append(
            f'<div class="pipeline-step {state}">'
            f'<span class="pipeline-marker">{marker}</span>'
            f'<span>{label}</span></div>'
        )
    writing = (
        '<div class="writing-indicator"><span class="dot"></span>'
        '<span class="dot"></span><span class="dot"></span>'
        '<span>Writing the answer</span></div>'
        if stage == "write" else ""
    )
    retrieval = (
        f'<div class="pipeline-count">{retrieved_count} passages retrieved</div>'
        if retrieved_count else ""
    )
    return (
        '<div class="pipeline-card"><div class="pipeline-label">LIVE PIPELINE</div>'
        '<div class="pipeline-steps">' + "".join(items) + '</div>'
        + retrieval + writing + '</div>'
    )
