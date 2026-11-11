"""All StudySense styling lives here. One accent colour (teal) used everywhere."""
import streamlit as st

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root{
  --font-display:'Bricolage Grotesque',system-ui,sans-serif;
  --font-body:'IBM Plex Sans',system-ui,sans-serif;
  --font-mono:'IBM Plex Mono',ui-monospace,monospace;
  --bg:#0d1218; --surface:#141c25; --surface2:#1b2631; --line:#293543;
  --fg:#e9eef3; --muted:#8c9cad;
  --accent:#4fc9bf; --accent-ink:#06201e;
  --good:#6fd58f; --bad:#f2786f;
}

/* ---------- base ---------- */
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--fg);font-family:var(--font-body)!important}
[data-testid="stHeader"]{background:transparent!important}
[data-testid="stToolbar"], #MainMenu, footer{visibility:hidden}
[data-testid="stMainBlockContainer"], .block-container{max-width:1240px;padding-top:2.2rem;padding-bottom:3rem}
h1,h2,h3,h4{font-family:var(--font-display)!important;letter-spacing:-.01em;color:var(--fg)}
p, li, label, span{font-family:var(--font-body)}
a{color:var(--accent)}
:focus-visible{outline:2px solid var(--accent)!important;outline-offset:2px}
.label{font:500 11px/1 var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.mono{font-family:var(--font-mono)}
.muted{color:var(--muted)}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--line)}
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{padding-top:1.6rem}
.brand{font:800 1.7rem/1 var(--font-display);letter-spacing:-.02em;margin-bottom:.4rem}
.hl{position:relative;isolation:isolate;display:inline-block;padding:0 .14em;margin-left:.04em;color:var(--accent-ink);animation:inkflip 1s .35s both}
.hl::before{content:"";position:absolute;inset:.06em 0 .02em;background:var(--accent);border-radius:3px;z-index:-1;transform-origin:left;animation:swipe 1s .35s both cubic-bezier(.7,0,.2,1)}
@keyframes swipe{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes inkflip{0%,45%{color:var(--fg)}65%,100%{color:var(--accent-ink)}}

.doccard{display:flex;gap:12px;align-items:center;background:var(--surface2);border:1px solid var(--line);border-radius:14px;padding:12px 14px}
.pdfico{width:34px;height:42px;border-radius:5px;background:var(--surface);border:1px solid var(--line);display:grid;place-items:center;font:600 9px var(--font-mono);color:var(--accent);flex:none}
.fname{font-weight:600;font-size:14px;overflow-wrap:anywhere;line-height:1.3}
.ringrow{display:flex;align-items:center;gap:16px;margin:6px 0}
.ring{width:84px;height:84px;flex:none;transform:rotate(-90deg)}
.ring circle{fill:none;stroke-width:7}
.ring .t{stroke:var(--surface2)}
.ring .v{stroke:var(--accent);stroke-linecap:round;stroke-dasharray:213.6;stroke-dashoffset:var(--off,0);animation:ringfill 1.6s cubic-bezier(.2,.8,.2,1) both}
@keyframes ringfill{from{stroke-dashoffset:213.6}}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:12px;flex:1}
.stat b{display:block;font:700 1.7rem/1.1 var(--font-display);font-variant-numeric:tabular-nums;margin-top:6px}
.sidehead{margin:18px 0 8px}
.kval{font:600 13px var(--font-mono);background:var(--accent);color:var(--accent-ink);border-radius:6px;padding:2px 8px}
.hint{font-size:12px;color:var(--muted);line-height:1.5}

/* live pipeline */
.flow{list-style:none;margin:0;padding:0;display:flex;flex-direction:column}
.flow li{position:relative;padding:0 0 16px 28px;font-size:13px;color:var(--muted)}
.flow li:last-child{padding-bottom:0}
.flow li::before{content:"";position:absolute;left:0;top:3px;width:12px;height:12px;border-radius:50%;border:2px solid var(--line);background:var(--surface);transition:all .3s}
.flow li::after{content:"";position:absolute;left:5px;top:17px;bottom:-3px;width:2px;background:var(--line)}
.flow li:last-child::after{display:none}
.flow li b{display:block;color:var(--fg);font-weight:600;font-size:13.5px}
.flow li span{font:400 11.5px var(--font-mono)}
.flow li.done::before{background:var(--accent);border-color:var(--accent)}
.flow li.done::after{background:var(--accent)}
.flow li.active::before{background:var(--accent);border-color:var(--accent);box-shadow:0 0 0 5px color-mix(in srgb,var(--accent) 25%,transparent);animation:beat 1s infinite}
.flow li.pending b{color:var(--muted)}
@keyframes beat{50%{box-shadow:0 0 0 9px color-mix(in srgb,var(--accent) 0%,transparent)}}

/* ---------- hero + document map ---------- */
.herotop{display:flex;flex-wrap:wrap;gap:12px 24px;justify-content:space-between;align-items:flex-end;margin-bottom:22px}
.hero h1{font:800 clamp(2.4rem,4.6vw,3.7rem)/1.02 var(--font-display)!important;margin:0;padding:0}
.hero p{margin:12px 0 0;color:var(--muted);max-width:64ch;font-size:1.02rem}
.hitlabel{font:500 12px var(--font-mono);color:var(--accent);display:flex;align-items:center;gap:8px}
.hitlabel i{width:8px;height:8px;border-radius:50%;background:var(--accent);animation:beat2 1.6s infinite}
@keyframes beat2{50%{opacity:.25}}
.strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(38px,62px));gap:8px;justify-content:start}
.pg{display:flex;flex-direction:column;gap:5px}
.pgbox{aspect-ratio:3/4;border:1px solid var(--line);border-radius:6px;background:var(--surface2);display:flex;flex-direction:column;gap:3px;padding:4px;transition:transform .25s,border-color .25s}
.strip.boot .pg{animation:rise .6s both;animation-delay:calc(var(--i)*55ms)}
@keyframes rise{from{opacity:0;transform:translateY(14px) rotate(-3deg)}}
.pg:hover .pgbox{transform:translateY(-4px);border-color:var(--accent)}
.ck{flex:1;position:relative;border-radius:3px;background-color:var(--surface);
  background-image:repeating-linear-gradient(to bottom,var(--line) 0 1px,transparent 1px 5px);
  animation:scan 7s linear infinite;animation-delay:calc(var(--i)*.24s)}
@keyframes scan{0%,10%,100%{background-color:var(--surface)}4%{background-color:color-mix(in srgb,var(--accent) 45%,var(--surface))}}
.strip.searching .ck{animation:scan 1s linear infinite;animation-delay:calc(var(--i)*.06s)}
.ck.hit{background-color:color-mix(in srgb,var(--accent) 38%,var(--surface));animation:pulse 1.8s ease-in-out infinite;
  box-shadow:0 0 0 1px var(--accent),0 0 14px color-mix(in srgb,var(--accent) 55%,transparent)}
.ck.hit span{position:absolute;inset:0;display:grid;place-items:center;font:600 10px var(--font-mono);color:var(--fg);animation:pop .35s both}
@keyframes pulse{50%{box-shadow:0 0 0 1px var(--accent),0 0 24px color-mix(in srgb,var(--accent) 80%,transparent)}}
@keyframes pop{from{transform:scale(2.2);opacity:0}}
.pgn{font:500 10px var(--font-mono);color:var(--muted);text-align:center}
.pgn.hit{color:var(--accent);font-weight:600}
.legend{display:flex;flex-wrap:wrap;gap:6px 22px;font:400 12px var(--font-mono);color:var(--muted);margin-top:16px}
.legend span{display:flex;gap:8px;align-items:center}
.legend i{width:10px;height:10px;border-radius:2px;display:inline-block}

/* ---------- native widgets ---------- */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]){border-color:var(--line)}
div[data-testid="stVerticalBlockBorderWrapper"][class*="st-emotion"]{border-radius:16px}

/* tabs */
[data-baseweb="tab-list"]{gap:4px;border-bottom:1px solid var(--line)}
[data-baseweb="tab"]{background:transparent!important;padding:12px 16px!important;height:auto!important}
[data-baseweb="tab"] p{font:500 15px var(--font-body)!important;color:var(--muted)}
[data-baseweb="tab"]:hover p{color:var(--fg)}
[data-baseweb="tab"][aria-selected="true"] p{color:var(--fg)}
[data-baseweb="tab-highlight"]{background:var(--accent)!important;height:3px!important;border-radius:3px 3px 0 0;transition:left .38s cubic-bezier(.3,.9,.3,1),width .38s cubic-bezier(.3,.9,.3,1)!important}
[data-baseweb="tab-border"]{background:transparent!important}
[data-baseweb="tab-panel"]{padding-top:1.4rem!important;animation:fadeup .4s both}
@keyframes fadeup{from{opacity:0;transform:translateY(10px)}}

/* buttons */
.stButton > button, [data-testid="stDownloadButton"] > button, [data-testid^="stBaseButton-secondary"]{
  background:transparent;color:var(--fg);border:1px solid var(--line);border-radius:10px;font:500 14px var(--font-body);
  padding:.5rem 1rem;min-height:44px;transition:border-color .2s,background .2s,transform .15s}
.stButton > button:hover, [data-testid="stDownloadButton"] > button:hover{border-color:var(--accent);background:var(--surface2);color:var(--fg)}
[data-testid^="stBaseButton-primary"]{background:var(--accent)!important;color:var(--accent-ink)!important;border:0!important;border-radius:10px;font-weight:600;min-height:44px;transition:transform .15s,box-shadow .15s}
[data-testid^="stBaseButton-primary"] p{color:var(--accent-ink)!important;font-weight:600}
[data-testid^="stBaseButton-primary"]:hover{transform:translateY(-2px);box-shadow:0 6px 0 -2px color-mix(in srgb,var(--accent) 40%,transparent)}

/* inputs */
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div, [data-testid="stNumberInput"] [data-baseweb="input"]{
  background:var(--surface2)!important;border-color:var(--line)!important;border-radius:10px!important}
[data-baseweb="input"]:focus-within, [data-baseweb="select"]:focus-within > div{border-color:var(--accent)!important}
[data-testid="InputInstructions"]{display:none}
input{font-family:var(--font-body)!important;color:var(--fg)!important}
[data-testid="stForm"]{border:1px solid var(--line);border-radius:16px;padding:18px;background:var(--surface)}
.stTextInput label p, .stSelectbox label p, .stSlider label p, .stNumberInput label p{color:var(--muted);font-size:13px}
[data-testid="stSlider"] [data-testid="stTickBarMin"], [data-testid="stSlider"] [data-testid="stTickBarMax"]{color:var(--muted);font-family:var(--font-mono);font-size:11px}
[data-testid="stSliderThumbValue"]{font-family:var(--font-mono);color:var(--accent)}

/* expanders */
[data-testid="stExpander"]{border:1px solid var(--line)!important;border-radius:12px;background:var(--surface);overflow:hidden}
[data-testid="stExpander"] summary{background:var(--surface2);padding:.75rem 1rem}
[data-testid="stExpander"] summary p{font-weight:500}

/* file uploader */
[data-testid="stFileUploaderDropzone"]{background:var(--surface2);border:2px dashed var(--line);border-radius:18px;padding:22px;transition:border-color .2s,background .2s}
[data-testid="stFileUploaderDropzone"]:hover{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 6%,var(--surface2))}
[data-testid="stFileUploaderDropzone"] button{background:var(--accent);color:var(--accent-ink);border:0;font-weight:600;border-radius:10px}
[data-testid="stFileUploaderDropzone"] button:hover{background:var(--accent);color:var(--accent-ink);transform:translateY(-2px)}
[data-testid="stFileUploaderDropzone"] small{font-family:var(--font-mono);color:var(--muted)}
.st-key-main_drop [data-testid="stFileUploaderDropzone"]{min-height:170px;justify-content:center;align-items:center;flex-direction:column;text-align:center;gap:10px}
.st-key-main_drop [data-testid="stFileUploaderDropzone"] > div{display:flex;flex-direction:column;align-items:center;text-align:center}
.st-key-main_drop [data-testid="stFileUploaderDropzoneInstructions"]{flex-direction:column;align-items:center;text-align:center}
[data-testid="stFileUploader"] section + div{display:none}

/* suggestion pills */
.st-key-sugg [data-testid="stVerticalBlock"]{flex-direction:row;flex-wrap:wrap;gap:8px}
.st-key-sugg [data-testid="stElementContainer"]{width:auto!important}
.st-key-sugg button{border-radius:999px;min-height:34px;padding:.2rem .9rem;font-size:13px;background:var(--surface2);animation:fadeup .4s both}

/* chat */
.msgstart{display:flex;flex-direction:column;gap:10px;padding-top:20px;margin-top:14px;border-top:1px solid var(--line);animation:fadeup .4s both}
.qtext{font:700 1.35rem/1.25 var(--font-display);margin-bottom:6px}
.pgtag{font:500 11px var(--font-mono);background:var(--accent);color:var(--accent-ink);padding:1px 6px;border-radius:5px;white-space:nowrap;margin:0 1px}
.chips{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:6px 0 10px}
.chip{font:500 12px var(--font-mono);border:1px solid var(--line);background:var(--surface2);border-radius:999px;padding:4px 12px;transition:all .2s;animation:fadeup .4s both;color:var(--fg)}
.chip:hover{background:var(--accent);color:var(--accent-ink);border-color:var(--accent);transform:translateY(-2px)}
.pass{padding:14px 4px;border-top:1px solid var(--line);font-size:14px;line-height:1.6}
.pass:first-child{border-top:0}
.pmeta{display:flex;justify-content:space-between;gap:12px;margin-bottom:6px;font-size:13px}
.pmeta .rk{font:500 11px var(--font-mono);color:var(--accent)}
.think{display:flex;gap:10px;align-items:center;color:var(--muted);font:400 13px var(--font-mono);padding:6px 0}
.dots{display:inline-flex;gap:4px}.dots i{width:6px;height:6px;border-radius:50%;background:var(--accent);animation:bounce 1s infinite}
.dots i:nth-child(2){animation-delay:.15s}.dots i:nth-child(3){animation-delay:.3s}
@keyframes bounce{50%{transform:translateY(-5px);opacity:.4}}

/* quiz */
.qhead{display:flex;flex-direction:column;gap:8px;margin-bottom:4px}
.qhead h3{font-size:1.1rem;margin:0;padding:0}
[data-testid="stRadio"], [data-testid="stElementContainer"]:has(> [data-testid="stRadio"]){width:100%!important}
[role="radiogroup"], [role="radiogroup"] > div:has(> label){display:grid!important;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:8px;width:100%}
[role="radiogroup"] label{background:var(--surface2);border:1px solid var(--line);border-radius:10px;padding:10px 14px!important;margin:0!important;transition:all .2s;cursor:pointer;width:100%}
[role="radiogroup"] label:hover{border-color:var(--accent)}
[role="radiogroup"] label:has(input:checked){background:var(--accent);border-color:var(--accent)}
[role="radiogroup"] label:has(input:checked) p{color:var(--accent-ink)!important;font-weight:600}
[role="radiogroup"] label > div:first-child{display:none}
label[data-testid="stRadioOption"] > div > div:first-child{display:none}
.result{display:flex;gap:22px;align-items:center;flex-wrap:wrap;animation:fadeup .5s both;margin:10px 0 6px}
.result .ring{width:110px;height:110px}
.score{font:800 2.6rem/1 var(--font-display);font-variant-numeric:tabular-nums}
.rev{border:1px solid var(--line);border-left-width:4px;border-radius:12px;padding:12px 16px;margin-top:10px;background:var(--surface);font-size:14px;line-height:1.55}
.rev.ok{border-left-color:var(--good)}.rev.no{border-left-color:var(--bad)}
.rev b.ok{color:var(--good)}.rev b.no{color:var(--bad)}
.rev .ex{color:var(--muted);font-size:13px;margin-top:4px}

/* key terms */
.terms{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:12px;margin-top:10px}
.term{border:1px solid var(--line);border-radius:14px;padding:14px 16px;background:var(--surface);display:flex;flex-direction:column;gap:6px;animation:fadeup .4s both;transition:transform .2s,border-color .2s}
.term:hover{transform:translateY(-3px);border-color:var(--accent)}
.term .tt{font:700 1.05rem var(--font-display);display:flex;justify-content:space-between;gap:10px;align-items:baseline}
.term p{margin:0;font-size:14px;color:var(--muted)}

/* progress */
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.metric{border:1px solid var(--line);border-radius:14px;padding:14px 16px;background:var(--surface)}
.metric b{display:block;font:800 2.1rem/1.1 var(--font-display);font-variant-numeric:tabular-nums;margin-top:8px}
.chart{display:grid;grid-template-columns:36px 1fr;gap:8px;height:230px;margin:34px 0 18px}
.yax{display:flex;flex-direction:column;justify-content:space-between;font:400 11px var(--font-mono);color:var(--muted);text-align:right;padding-bottom:24px}
.plot{position:relative;display:flex;gap:18px;align-items:flex-end;padding:0 14px 24px;border-left:1px solid var(--line);
  background:repeating-linear-gradient(to top,transparent 0 calc(25% - 1px),var(--line) calc(25% - 1px) 25%);background-size:100% calc(100% - 24px);background-repeat:no-repeat}
.bar{flex:1;max-width:90px;position:relative;height:calc(var(--v)*1%);background:var(--accent);border-radius:6px 6px 0 0;transform-origin:bottom;animation:growbar .9s both cubic-bezier(.2,.8,.2,1);animation-delay:calc(var(--n)*160ms)}
@keyframes growbar{from{transform:scaleY(0)}}
.bar em{position:absolute;top:-22px;left:0;right:0;text-align:center;font:600 12px var(--font-mono);font-style:normal}
.bar u{position:absolute;bottom:-22px;left:0;right:0;text-align:center;font:400 11px var(--font-mono);text-decoration:none;color:var(--muted)}

/* empty state */
.floaters{position:relative;width:150px;height:110px;margin:0 auto 8px}
.floaters i{position:absolute;width:62px;height:80px;border-radius:6px;border:1px solid var(--line);background:var(--surface2);left:44px;top:14px;animation:float 4s ease-in-out infinite;
  background-image:repeating-linear-gradient(to bottom,var(--line) 0 2px,transparent 2px 9px);background-size:100% 56px;background-repeat:no-repeat;background-position:0 14px}
.floaters i:nth-child(1){transform:translateX(-46px) rotate(-12deg);animation-delay:-1s}
.floaters i:nth-child(3){transform:translateX(46px) rotate(12deg);animation-delay:-2s}
.floaters i:nth-child(2){z-index:1;border-color:var(--accent)}
@keyframes float{50%{translate:0 -9px}}
.dropcopy{text-align:center;margin-bottom:12px}
.dropcopy h3{font-size:1.25rem;margin:0}
.emptyh1{font:800 clamp(2.3rem,4.4vw,3.6rem)/1.04 var(--font-display);margin:0 0 14px;letter-spacing:-.02em}
.feat{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-top:28px}
.feat div{border:1px solid var(--line);border-radius:14px;padding:14px 16px;background:var(--surface);transition:transform .2s,border-color .2s;display:flex;flex-direction:column;gap:6px}
.feat div:hover{transform:translateY(-4px);border-color:var(--accent)}
.feat b{font:700 1.05rem var(--font-display)}.feat span{font-size:13.5px;color:var(--muted)}
.feat em{font:500 11px var(--font-mono);font-style:normal;color:var(--accent)}
.footer{text-align:center;color:var(--muted);margin-top:3rem;font:400 12px var(--font-mono)}
.pageinfo{font-size:14px;color:var(--muted);margin:8px 0 12px}

@media (prefers-reduced-motion: reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
"""


def inject_css():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)