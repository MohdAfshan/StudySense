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
