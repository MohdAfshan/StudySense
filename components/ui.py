import html


def esc(text):
    return html.escape(str(text))


def hero():
    return """
    <div class="hero">
      <h1>StudySense</h1>
      <p>Your AI study partner. Upload a PDF, ask questions with page references,
      get summaries, quizzes, flashcards and key terms.</p>
    </div>
    """


def feature_card(title, description):
    return f'<div class="feature-card"><b>{esc(title)}</b><br>{esc(description)}</div>'


def source_card(text, page):
    return (
        f'<div class="source-card"><b>Page {esc(page)}</b><br>{esc(text)}</div>'
    )


def source_chips(pages):
    return "".join(f'<span class="chip">Page {esc(page)}</span>' for page in pages)


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
