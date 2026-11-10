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

[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
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
    color: var(--study-teal);
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
    background: var(--study-teal-soft);
    border-color: var(--study-teal);
}

.term-card {
    background: var(--study-surface);
    color: var(--study-text);
    border-left: 4px solid var(--study-teal);
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
}
"""


def inject_styles():
    st.markdown(f"<style>{STUDY_DESK_CSS}</style>", unsafe_allow_html=True)
