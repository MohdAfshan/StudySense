"""HTML builders for StudySense. Every function returns a single compact HTML string
(no blank lines, no indentation) so Streamlit's markdown parser leaves it untouched."""
import html
import json
import re


def esc(text):
    return html.escape(str(text))


def one(text):
    """Collapse whitespace/newlines so passage text is safe inside an HTML block."""
    return re.sub(r"\s+", " ", str(text)).strip()


# ---------------------------------------------------------------- sidebar
def wordmark():
    return '<div class="brand">Study<span class="hl">Sense</span></div>'


def doc_card(name, size_kb=None):
    size = f'<div class="label" style="margin-top:7px">{size_kb:.1f} KB</div>' if size_kb else ""
    return (f'<div class="doccard"><div class="pdfico">PDF</div>'
            f'<div><div class="fname">{esc(name)}</div>{size}</div></div>')


def empty_doc_card():
    return ('<div class="doccard"><div class="pdfico">PDF</div><div><div class="fname">No file yet</div>'
            '<div class="label" style="margin-top:7px">PDF with a text layer</div></div></div>')


def ring_stats(pages, chunks):
    return ('<div class="ringrow"><svg class="ring" viewBox="0 0 84 84" aria-hidden="true">'
            '<circle class="t" cx="42" cy="42" r="34"/><circle class="v" cx="42" cy="42" r="34"/></svg>'
            f'<div class="stats"><div class="stat"><span class="label">Pages</span><b>{pages}</b></div>'
            f'<div class="stat"><span class="label">Chunks</span><b>{chunks}</b></div></div></div>')


def session_stats(asked, quizzes):
    return ('<div class="stats" style="margin-top:6px">'
            f'<div class="stat"><span class="label">Questions</span><b>{asked}</b></div>'
            f'<div class="stat"><span class="label">Quizzes</span><b>{quizzes}</b></div></div>')


def label(text):
    return f'<div class="label sidehead">{esc(text)}</div>'


def passages_pill(k):
    return (f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:4px">'
            f'<span style="font-size:13px;color:var(--muted)">Passages to retrieve</span><span class="kval">{k}</span></div>')


def pipeline(state, chunks, k):
    """state: -1 idle, 0..3 = that step is active, 4 = everything done."""
    steps = [("Embed the question", "all-MiniLM-L6-v2"),
             ("Search the chunks", f"ChromaDB · {chunks} chunks"),
             ("Retrieve the best passages", f"top {k} by similarity"),
             ("Write the answer", "llama3.1:8b on Ollama")]
    items = []
    for i, (title, sub) in enumerate(steps):
        cls = "done" if i < state else ("active" if i == state else "pending")
        items.append(f'<li class="{cls}"><b>{title}</b><span>{sub}</span></li>')
    return f'<ol class="flow">{"".join(items)}</ol>'


# ---------------------------------------------------------------- hero + document map
def docmap(pages, chunks, hits, mode="idle"):
    """hits: ordered list of page numbers (rank 1 first). mode: idle | searching | boot."""
    per = max(1, min(3, round(chunks / pages))) if pages else 1
    ranks = {}
    for r, p in enumerate(hits, 1):
        ranks.setdefault(int(p), []).append(r)
    cells = []
    for p in range(1, pages + 1):
        rk = ranks.get(p, [])
        cks = []
        for i in range(per):
            if i < len(rk):
                cks.append(f'<i class="ck hit" style="--i:{p + i}"><span>{rk[i]}</span></i>')
            else:
                cks.append(f'<i class="ck" style="--i:{p + i}"></i>')
        cls = "pgn hit" if rk else "pgn"
        cells.append(f'<div class="pg" style="--i:{p - 1}"><div class="pgbox">{"".join(cks)}</div><span class="{cls}">{p}</span></div>')
    extra = {"searching": " searching", "boot": " boot"}.get(mode, "")
    legend = ('<div class="legend"><span><i style="background:var(--surface2);border:1px solid var(--line)"></i>chunk being indexed</span>'
              '<span><i style="background:color-mix(in srgb,var(--accent) 45%,var(--surface));box-shadow:0 0 0 1px var(--accent)"></i>'
              'retrieved for the current question, numbered by rank</span></div>')
    return f'<div class="strip{extra}" aria-label="Document map">{"".join(cells)}</div>{legend}'


def hero(status):
    return ('<div class="hero"><div class="herotop"><div><h1>Study<span class="hl">Sense</span></h1>'
            '<p>Your AI study partner. Every answer is traced back to the pages it came from.</p></div>'
            f'<div class="hitlabel"><i></i><span>{esc(status)}</span></div></div></div>')


# ---------------------------------------------------------------- empty state
def empty_headline():
    return ('<div class="emptyh1">Turn any PDF into a <span class="hl">study session</span></div>'
            '<p class="muted" style="max-width:48ch;font-size:1.02rem">Upload your notes or a textbook chapter. '
            'StudySense reads it page by page, then answers with page references, writes summaries and builds '
            'quizzes, flashcards and a glossary from the same text.</p>'
            '<p class="mono muted" style="font-size:12.5px;margin-top:16px">Runs locally with Ollama. Your document never leaves this machine.</p>')


def drop_copy():
    return ('<div class="dropcopy"><div class="floaters"><i></i><i></i><i></i></div>'
            '<h3>Drop a PDF here</h3></div>')


def feature_cards():
    cards = [("Ask", "Answers that cite the page they came from.", "page refs + sources"),
             ("Summarize", "Short, detailed or exam revision style.", "page range"),
             ("Quiz", "Pick difficulty, get scored on the spot.", "easy · medium · hard"),
             ("Flashcards", "Flip through cards to memorize key ideas.", "front / back"),
             ("Key terms", "A searchable glossary of your document.", "downloadable")]
    return '<div class="feat">' + "".join(
        f'<div><b>{t}</b><span>{d}</span><em>{tag}</em></div>' for t, d, tag in cards) + '</div>'


# ---------------------------------------------------------------- ask
_REF = re.compile(r"\(\s*pages?\s*([0-9][0-9,\s\-–and&]*)\)", re.I)


def answer_md(text):
    """Turn '(Page 6)' / '(Pages 3, 5)' into small teal tags. Everything else stays markdown."""
    def sub(m):
        nums = re.findall(r"\d+", m.group(1))
        return " ".join(f'<span class="pgtag">p.{n}</span>' for n in nums)
    return _REF.sub(sub, str(text))


def question_block(q):
    return f'<div class="msgstart"><span class="label">You</span><div class="qtext">{esc(q)}</div></div>'


def thinking(text):
    return f'<div class="think"><span class="dots"><i></i><i></i><i></i></span><span>{esc(text)}</span></div>'


def source_chips(pages):
    uniq = sorted({int(p) for p in pages})
    chips = "".join(f'<span class="chip" style="animation-delay:{i * 90}ms">Page {p}</span>' for i, p in enumerate(uniq))
    return f'<div class="chips"><span class="label" style="margin-right:4px">Sources</span>{chips}</div>'


def source_cards(sources):
    out = []
    for i, (text, meta) in enumerate(sources, 1):
        out.append(f'<div class="pass"><div class="pmeta"><b>Page {esc(meta.get("page", "?"))}</b>'
                   f'<span class="rk">rank {i}</span></div><div>{esc(one(text))}</div></div>')
    return "".join(out)


# ---------------------------------------------------------------- quiz
def quiz_head(i, item):
    return (f'<div class="qhead"><span class="label">Q{i + 1} · Page {esc(item.get("page", "?"))}</span>'
            f'<h3>{esc(item["question"])}</h3></div>')


def quiz_result(score, total, quiz, answers):
    off = 213.6 * (1 - (score / total if total else 0))
    reviews = []
    for i, item in enumerate(quiz):
        chosen = answers[i]
        ok = chosen == item["answer"]
        verdict = '<b class="ok">Correct</b>' if ok else '<b class="no">Not quite</b>'
        extra = "" if ok else f'<div>You chose: {esc(chosen) if chosen else "Not answered"}. Correct answer: <b>{esc(item["answer"])}</b></div>'
        ex = f'<div class="ex">{esc(item["explanation"])}</div>' if item.get("explanation") else ""
        reviews.append(f'<div class="rev {"ok" if ok else "no"}"><div>{verdict} · Q{i + 1} · Page {esc(item.get("page", "?"))}</div>{extra}{ex}</div>')
    return ('<div class="result"><svg class="ring" viewBox="0 0 84 84" aria-hidden="true">'
            f'<circle class="t" cx="42" cy="42" r="34"/><circle class="v" cx="42" cy="42" r="34" style="--off:{off:.1f};stroke:var(--good)"/></svg>'
            f'<div><div class="label">Your score</div><div class="score">{score} / {total}</div></div></div>'
            + "".join(reviews))


# ---------------------------------------------------------------- key terms
def term_cards(terms):
    if not terms:
        return '<div class="hint">No terms match that search.</div>'
    cards = "".join(
        f'<div class="term" style="animation-delay:{i * 60}ms"><div class="tt">{esc(t["term"])}<span class="pgtag">p.{esc(t["page"])}</span></div>'
        f'<p>{esc(t["definition"])}</p></div>' for i, t in enumerate(terms))
    return f'<div class="terms">{cards}</div>'


# ---------------------------------------------------------------- progress
def metrics(asked, quizzes, avg, best):
    def m(lbl, val):
        return f'<div class="metric"><span class="label">{lbl}</span><b>{val}</b></div>'
    return ('<div class="metrics">' + m("Questions asked", asked) + m("Quizzes taken", quizzes)
            + m("Average score", avg) + m("Best score", best) + '</div>')


def bar_chart(scores):
    bars = "".join(f'<div class="bar" style="--v:{s};--n:{i}"><em>{s}%</em><u>Quiz {i + 1}</u></div>' for i, s in enumerate(scores))
    return ('<div class="label" style="margin-top:22px">Quiz scores</div><div class="chart"><div class="yax">'
            '<span>100</span><span>75</span><span>50</span><span>25</span><span>0</span></div>'
            f'<div class="plot">{bars}</div></div>')


def page_info(page, hit_ranks):
    if hit_ranks:
        txt = f'<span style="color:var(--accent)">Retrieved for your last question (rank {", ".join(map(str, hit_ranks))})</span>'
    else:
        txt = "Not used for your last question"
    return f'<div class="pageinfo"><b style="color:var(--fg)">Page {page}</b> · {txt}</div>'


def footer():
    return '<div class="footer">StudySense · Built with RAG, Streamlit and Ollama</div>'


# ---------------------------------------------------------------- flashcards (self-contained, runs in an iframe)
_FLASH = """<!doctype html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
:root{--bg:#0d1218;--surface2:#1b2631;--line:#293543;--fg:#e9eef3;--muted:#8c9cad;--accent:#4fc9bf;--ink:#06201e}
*{box-sizing:border-box}body{margin:0;background:transparent;color:var(--fg);font-family:'IBM Plex Sans',system-ui,sans-serif;display:flex;flex-direction:column;gap:14px;padding:2px}
.nav{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.mono{font:400 13px 'IBM Plex Mono',monospace}.hint{font-size:12px;color:var(--muted)}
.bar{height:5px;border-radius:5px;background:var(--surface2);overflow:hidden}.bar i{display:block;height:100%;background:var(--accent);transition:width .4s}
.fc{perspective:1400px;height:230px;cursor:pointer;outline:none}
.fci{position:relative;height:100%;transition:transform .65s cubic-bezier(.2,.8,.2,1);transform-style:preserve-3d}
.fc.flip .fci{transform:rotateY(180deg)}
.face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;border-radius:18px;display:grid;place-items:center;text-align:center;padding:40px 30px;font:700 clamp(1.15rem,2.6vw,1.65rem)/1.3 'Bricolage Grotesque',sans-serif}
.face small{position:absolute;top:16px;left:20px;font:500 11px 'IBM Plex Mono',monospace;letter-spacing:.08em;text-transform:uppercase}
.front{background:var(--surface2);border:1px solid var(--line)}.front small{color:var(--muted)}
.back{background:var(--accent);color:var(--ink);transform:rotateY(180deg);font-weight:700}.back small{opacity:.7}
.fc:focus-visible .face{outline:2px solid var(--fg)}
.btns{display:flex;gap:10px;justify-content:space-between}
button{font:500 14px 'IBM Plex Sans',sans-serif;color:var(--fg);background:transparent;border:1px solid var(--line);border-radius:10px;padding:10px 18px;cursor:pointer;min-height:44px;transition:all .2s;flex:1}
button:hover{border-color:var(--accent);background:var(--surface2)}
button.p{background:var(--accent);color:var(--ink);border:0;font-weight:600}button.p:hover{transform:translateY(-2px);background:var(--accent)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style></head><body>
<div class="nav"><span class="mono" id="cnt"></span><span class="hint">Click the card or press Space to flip. Arrow keys move between cards.</span></div>
<div class="bar"><i id="bar"></i></div>
<div class="fc" id="fc" tabindex="0" role="button" aria-label="Flashcard. Press to flip"><div class="fci">
<div class="face front"><small>Question</small><span id="f"></span></div>
<div class="face back"><small>Answer</small><span id="b"></span></div></div></div>
<div class="btns"><button id="pv">Previous</button><button class="p" id="fl">Flip card</button><button id="nx">Next</button></div>
<script>
const D=__DATA__;let i=0;const $=id=>document.getElementById(id),fc=$('fc');
function show(){const c=D[i];fc.classList.remove('flip');$('f').textContent=c.front;$('b').textContent=c.back;
$('cnt').textContent='Card '+(i+1)+' of '+D.length+' · Page '+c.page;$('bar').style.width=((i+1)/D.length*100)+'%'}
const flip=()=>fc.classList.toggle('flip');
fc.onclick=flip;$('fl').onclick=flip;
$('nx').onclick=()=>{i=(i+1)%D.length;show()};$('pv').onclick=()=>{i=(i-1+D.length)%D.length;show()};
document.addEventListener('keydown',e=>{if(e.key===' '){e.preventDefault();flip()}else if(e.key==='ArrowRight')$('nx').click();else if(e.key==='ArrowLeft')$('pv').click()});
show();
</script></body></html>"""


def flashcards_html(cards):
    data = [{"front": str(c.get("front", "")), "back": str(c.get("back", "")), "page": str(c.get("page", "?"))} for c in cards]
    payload = json.dumps(data).replace("</", "<\\/")
    return _FLASH.replace("__DATA__", payload)