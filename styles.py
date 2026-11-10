import streamlit as st


STUDY_DESK_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {
    --study-bg: #101923;
    --study-surface: #182532;
    --study-surface-raised: #203140;
    --study-border: #2b3d4c;
    --study-border-strong: #3a5263;
    --study-text: #e7edf0;
    --study-muted: #9eafb9;
    --study-yellow: #f5d547;
    --study-yellow-soft: #332f1a;
    --study-teal: #55c5bb;
    --study-teal-soft: #173c3d;
    --study-green: #70d39b;
    --study-red: #ed7d7d;
    --study-heading: "Bricolage Grotesque", sans-serif;
    --study-body: "IBM Plex Sans", sans-serif;
    --study-mono: "IBM Plex Mono", monospace;
    --study-radius: 12px;
    --study-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
}

@property --ring-progress {
    syntax: "<percentage>";
    inherits: false;
    initial-value: 0%;
}

@property --count-pages {
    syntax: "<integer>";
    inherits: false;
    initial-value: 0;
}

@property --count-chunks {
    syntax: "<integer>";
    inherits: false;
    initial-value: 0;
}

html, body, [class*="css"] {
    font-family: var(--study-body);
}

body, .stApp, [data-testid="stAppViewContainer"] {
    background: var(--study-bg);
    color: var(--study-text);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1440px;
    padding-top: 2rem;
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--study-heading);
    color: var(--study-text);
    letter-spacing: -0.02em;
}

p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
    color: var(--study-text);
}

[data-testid="stSidebar"] {
    background: var(--study-surface);
    border-right: 1px solid var(--study-border);
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: var(--study-heading);
}

button, [data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button {
    border: 1px solid var(--study-border-strong);
    border-radius: 8px;
    background: var(--study-surface-raised);
    color: var(--study-text);
    font-family: var(--study-body);
    font-weight: 600;
    transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
}

button:hover, [data-testid="stButton"] button:hover, [data-testid="stFormSubmitButton"] button:hover {
    border-color: var(--study-yellow);
    background: var(--study-yellow-soft);
    color: var(--study-yellow);
}

[data-testid="stFormSubmitButton"] button {
    border-color: var(--study-yellow);
    background: var(--study-yellow);
    color: var(--study-bg);
}

[data-testid="stFormSubmitButton"] button:hover {
    background: var(--study-yellow);
    color: var(--study-bg);
    transform: translateY(-2px);
}

[data-testid="stDownloadButton"] button {
    border-color: var(--study-yellow);
    color: var(--study-yellow);
}

input, textarea, [data-baseweb="select"] > div, [data-testid="stNumberInput"] input {
    border-color: var(--study-border-strong) !important;
    border-radius: 8px !important;
    background: var(--study-surface) !important;
    color: var(--study-text) !important;
}

input:focus, textarea:focus, [data-baseweb="select"] > div:focus-within {
    border-color: var(--study-yellow) !important;
    box-shadow: 0 0 0 1px var(--study-yellow) !important;
}

[data-baseweb="popover"], [data-baseweb="menu"] {
    background: var(--study-surface-raised);
    border: 1px solid var(--study-border);
}

[role="option"]:hover, [aria-selected="true"] {
    background: var(--study-yellow-soft) !important;
    color: var(--study-yellow) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: var(--study-yellow);
    border-color: var(--study-yellow);
}

[data-testid="stSlider"] [data-baseweb="slider"] > div:first-child {
    background: var(--study-border-strong);
}

[data-testid="stSlider"] [data-baseweb="slider"] > div:nth-child(2) {
    background: var(--study-yellow);
}

[data-testid="stTabs"] [role="tablist"] {
    gap: 0.35rem;
    border-bottom: 1px solid var(--study-border);
}

[data-testid="stTabs"] button[role="tab"] {
    border: 0;
    border-bottom: 2px solid transparent;
    border-radius: 0;
    background: transparent;
    color: var(--study-muted);
    font-family: var(--study-heading);
}

[data-testid="stTabs"] button[role="tab"]:hover {
    color: var(--study-yellow);
    background: transparent;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    border-bottom-color: var(--study-yellow);
    color: var(--study-yellow);
}

[data-testid="stExpander"] {
    border: 1px solid var(--study-border);
    border-radius: var(--study-radius);
    background: var(--study-surface);
}

[data-testid="stExpander"] summary:hover {
    color: var(--study-yellow);
}

[data-testid="stChatMessage"] {
    border: 1px solid var(--study-border);
    border-radius: var(--study-radius);
    background: var(--study-surface);
    box-shadow: var(--study-shadow);
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    color: var(--study-text);
}

[data-testid="stMetric"] {
    border: 1px solid var(--study-border);
    border-radius: var(--study-radius);
    background: var(--study-surface);
    padding: 0.8rem 1rem;
}

[data-testid="stMetricLabel"], [data-testid="stMetricValue"],
[data-testid="stCaptionContainer"] {
    font-family: var(--study-mono);
}

[data-testid="stMetricLabel"] {
    color: var(--study-muted);
}

[data-testid="stMetricValue"] {
    color: var(--study-yellow);
}

[data-testid="stFileUploader"] section {
    border: 1px dashed var(--study-border-strong);
    border-radius: var(--study-radius);
    background: var(--study-surface-raised);
}

[data-testid="stFileUploader"] section:hover {
    border-color: var(--study-yellow);
}

[data-testid="stProgressBar"] > div > div {
    background: var(--study-yellow);
}

.sidebar-wordmark {
    display: flex;
    align-items: baseline;
    gap: 0.18rem;
    margin: 0.2rem 0 1.5rem;
    color: var(--study-text);
    font-family: var(--study-heading);
    font-size: 1.7rem;
    font-weight: 700;
    letter-spacing: -0.04em;
}

.wordmark-sense {
    position: relative;
    z-index: 0;
    color: var(--study-text);
}

.wordmark-sense::after {
    position: absolute;
    z-index: -1;
    right: -0.08em;
    bottom: 0.08em;
    left: -0.08em;
    height: 0.42em;
    border-radius: 3px;
    background: var(--study-yellow);
    content: "";
    transform: scaleX(0);
    transform-origin: left;
    animation: highlight-swipe 700ms cubic-bezier(0.2, 0.8, 0.2, 1) 350ms forwards;
}

.document-card {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.75rem;
    border: 1px solid var(--study-border);
    border-radius: var(--study-radius);
    background: var(--study-surface-raised);
}

.pdf-icon {
    display: grid;
    width: 2rem;
    height: 2.2rem;
    place-items: center;
    border: 1px solid var(--study-yellow);
    border-radius: 5px;
    color: var(--study-yellow);
    font-family: var(--study-mono);
    font-size: 0.55rem;
    font-weight: 600;
}

.document-details {
    display: grid;
    min-width: 0;
    gap: 0.18rem;
}

.document-details strong {
    overflow: hidden;
    color: var(--study-text);
    font-size: 0.9rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.document-details span {
    color: var(--study-muted);
    font-family: var(--study-mono);
    font-size: 0.7rem;
}

.indexing-summary {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.75rem 0;
}

.progress-ring {
    position: relative;
    display: grid;
    width: 4.2rem;
    height: 4.2rem;
    flex: 0 0 auto;
    place-items: center;
    border-radius: 50%;
    background: conic-gradient(var(--study-yellow) var(--ring-progress), var(--study-border) 0);
    animation: ring-fill 800ms ease-out;
}

.progress-ring::before {
    position: absolute;
    width: 3.45rem;
    height: 3.45rem;
    border-radius: 50%;
    background: var(--study-surface);
    content: "";
}

.ring-check {
    z-index: 1;
    color: var(--study-yellow);
    font-family: var(--study-mono);
    font-size: 0.58rem;
    font-weight: 600;
}

.indexing-counts {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
    flex: 1;
}

.indexing-counts div {
    display: grid;
    gap: 0.1rem;
}

.indexing-counts strong {
    color: var(--study-yellow);
    font-family: var(--study-mono);
    font-size: 1.15rem;
}

.indexing-counts strong::after {
    display: inline-block;
    animation-duration: 900ms;
    animation-timing-function: ease-out;
    animation-fill-mode: forwards;
}

.indexing-counts .count-pages::after {
    content: counter(page-count);
    animation-name: count-pages;
}

.indexing-counts .count-chunks::after {
    content: counter(chunk-count);
    animation-name: count-chunks;
}

.indexing-counts .count-pages {
    counter-reset: page-count var(--count-pages);
    --count-pages: 0;
}

.indexing-counts .count-chunks {
    counter-reset: chunk-count var(--count-chunks);
    --count-chunks: 0;
}

.indexing-counts span {
    color: var(--study-muted);
    font-family: var(--study-mono);
    font-size: 0.68rem;
}

.value-pill {
    display: inline-block;
    margin-left: 0.4rem;
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
    background: var(--study-yellow);
    color: var(--study-bg);
    font-family: var(--study-mono);
    font-size: 0.72rem;
    font-weight: 600;
}

.settings-label, .pipeline-label {
    color: var(--study-muted);
    font-family: var(--study-mono);
    font-size: 0.66rem;
    letter-spacing: 0.1em;
}

.settings-hint {
    margin: -0.25rem 0 0.5rem;
    color: var(--study-muted);
    font-size: 0.75rem;
}

.pipeline-card {
    margin-top: 0.7rem;
    padding: 0.85rem;
    border: 1px solid var(--study-border);
    border-radius: var(--study-radius);
    background: var(--study-bg);
}

.pipeline-steps {
    position: relative;
    display: grid;
    gap: 0.55rem;
    margin-top: 0.7rem;
}

.pipeline-steps::before {
    position: absolute;
    top: 0.55rem;
    bottom: 0.55rem;
    left: 0.45rem;
    width: 1px;
    background: var(--study-border);
    content: "";
}

.pipeline-step {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: 0.55rem;
    color: var(--study-muted);
    font-size: 0.75rem;
}

.pipeline-marker {
    display: grid;
    width: 0.95rem;
    height: 0.95rem;
    place-items: center;
    border: 1px solid var(--study-border-strong);
    border-radius: 50%;
    background: var(--study-bg);
    font-family: var(--study-mono);
    font-size: 0.5rem;
}

.pipeline-step.complete {
    color: var(--study-teal);
}

.pipeline-step.complete .pipeline-marker {
    border-color: var(--study-teal);
    background: var(--study-teal);
    color: var(--study-bg);
}

.pipeline-step.complete::after {
    position: absolute;
    top: 1rem;
    bottom: -0.55rem;
    left: 0.45rem;
    width: 1px;
    background: var(--study-teal);
    content: "";
}

.pipeline-step.active {
    color: var(--study-yellow);
}

.pipeline-step.active .pipeline-marker {
    border-color: var(--study-yellow);
    color: var(--study-yellow);
    animation: marker-pulse 1.1s ease-in-out infinite;
}

.pipeline-count {
    margin-top: 0.65rem;
    color: var(--study-teal);
    font-family: var(--study-mono);
    font-size: 0.66rem;
}

.writing-indicator {
    display: flex;
    align-items: center;
    gap: 0.22rem;
    margin-top: 0.7rem;
    color: var(--study-yellow);
    font-family: var(--study-mono);
    font-size: 0.66rem;
}

.writing-indicator span:last-child {
    margin-left: 0.25rem;
}

.writing-indicator .dot {
    width: 0.28rem;
    height: 0.28rem;
    border-radius: 50%;
    background: var(--study-yellow);
    animation: dot-bounce 900ms ease-in-out infinite;
}

.writing-indicator .dot:nth-child(2) { animation-delay: 120ms; }
.writing-indicator .dot:nth-child(3) { animation-delay: 240ms; }

.document-map-wrap {
    margin-top: 0.8rem;
}

.document-map {
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    gap: 0.16rem;
    margin-top: 0.45rem;
}

.document-chunk {
    position: relative;
    display: grid;
    min-height: 0.6rem;
    place-items: center;
    border-radius: 2px;
    background: var(--study-border);
    color: var(--study-bg);
    font-family: var(--study-mono);
    font-size: 0.45rem;
}

.document-chunk.chunk-searching {
    animation: chunk-wave 700ms ease-in-out infinite;
}

.document-chunk.chunk-retrieved {
    background: var(--study-teal);
    animation: chunk-retrieve 350ms ease-out both;
}

@keyframes highlight-swipe {
    to { transform: scaleX(1); }
}

@keyframes ring-fill {
    from { --ring-progress: 0%; }
}

@keyframes count-pages {
    to { --count-pages: var(--target-pages); }
}

@keyframes count-chunks {
    to { --count-chunks: var(--target-chunks); }
}

@keyframes marker-pulse {
    50% { box-shadow: 0 0 0 4px var(--study-yellow-soft); }
}

@keyframes dot-bounce {
    50% { transform: translateY(-3px); }
}

@keyframes chunk-wave {
    50% { background: var(--study-yellow); box-shadow: 0 0 5px var(--study-yellow); }
}

@keyframes chunk-retrieve {
    from { opacity: 0.35; transform: scale(0.7); }
    to { opacity: 1; transform: scale(1); }
}

hr {
    border-color: var(--study-border);
}

.hero {
    background: var(--study-surface);
    border: 1px solid var(--study-border);
    border-left: 4px solid var(--study-yellow);
    padding: 2rem 2.5rem;
    border-radius: var(--study-radius);
    box-shadow: var(--study-shadow);
    margin-bottom: 1.2rem;
}

.hero h1 {
    margin: 0;
    color: var(--study-yellow);
    font-size: 2.6rem;
}

.hero p {
    margin: 0.4rem 0 0;
    color: var(--study-muted);
    font-size: 1.1rem;
}

.chip {
    display: inline-block;
    background: var(--study-teal-soft);
    border: 1px solid var(--study-teal);
    color: var(--study-teal);
    padding: 3px 10px;
    border-radius: 999px;
    font-family: var(--study-mono);
    font-size: 0.78rem;
    margin-right: 6px;
}

.source-card {
    background: var(--study-surface-raised);
    color: var(--study-text);
    border: 1px solid var(--study-border);
    padding: 0.8rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    font-size: 0.92rem;
}

.source-card b, .term-card .page-label {
    color: var(--study-yellow);
    font-family: var(--study-mono);
}

.flashcard {
    background: var(--study-surface);
    color: var(--study-text);
    border: 1px solid var(--study-yellow);
    border-radius: 16px;
    padding: 2.2rem 1.5rem;
    text-align: center;
    font-size: 1.35rem;
    min-height: 150px;
    margin-bottom: 0.8rem;
    box-shadow: var(--study-shadow);
}

.flashcard.back {
    background: var(--study-surface-raised);
    border-color: var(--study-yellow);
}

.term-card {
    background: var(--study-surface);
    color: var(--study-text);
    border-left: 4px solid var(--study-yellow);
    padding: 0.8rem 1.1rem;
    border-radius: 8px;
    margin-bottom: 0.6rem;
}

.feature-card {
    border: 1px solid var(--study-border);
    border-radius: var(--study-radius);
    padding: 1rem 1.2rem;
    height: 100%;
    background: var(--study-surface);
}

.feature-card b {
    color: var(--study-yellow);
    font-family: var(--study-heading);
}

.footer {
    text-align: center;
    color: var(--study-muted);
    margin-top: 3rem;
    font-family: var(--study-mono);
    font-size: 0.78rem;
}

.mono-label, .page-label {
    font-family: var(--study-mono);
    color: var(--study-muted);
}

.quiz-correct {
    color: var(--study-green);
}

.quiz-wrong {
    color: var(--study-red);
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
    }

    .wordmark-sense::after {
        transform: scaleX(1);
    }
}
"""


def inject_styles():
    st.markdown(f"<style>{STUDY_DESK_CSS}</style>", unsafe_allow_html=True)
