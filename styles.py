"""Feuille de style de Pavel IA CV (thème indigo, violet et turquoise)."""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:wght@400;500;700&display=swap');

:root {
  --midnight: #0D1033;
  --indigo: #4F46E5;
  --orchid: #8B5CF6;
  --lagoon: #14B8A6;
  --sun: #FFB84D;
  --cloud: #F5F7FF;
  --ink: #141A3C;
  --line: #E0E4F5;
  --muted: #626A8F;
}

html, body, .stApp, [data-testid="stAppViewContainer"], .stMarkdown, label, input, textarea, button {
  font-family: 'DM Sans', sans-serif;
}
.stApp {
  color: var(--ink);
  background:
    radial-gradient(900px 520px at 108% -6%, rgba(139, 92, 246, .22), transparent 60%),
    radial-gradient(720px 440px at -12% 10%, rgba(20, 184, 166, .16), transparent 55%),
    var(--cloud);
  background-attachment: fixed;
}
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 860px; padding: 2.4rem 1.1rem 3rem; }
@media (max-width: 640px) { .block-container { padding-top: 3.2rem; } }

h1, h2, h3, h4, h5 {
  font-family: 'Bricolage Grotesque', sans-serif; letter-spacing: -0.015em; color: var(--ink);
}
h2 { font-size: 1.7rem; font-weight: 800; }
[data-testid="stCaptionContainer"] { color: var(--muted); }

/* ── Barre du haut ─────────────────────────────────────── */
.nav { display: flex; align-items: center; justify-content: space-between; margin: 0 .2rem 1rem; }
.nav .brand { display: flex; align-items: center; gap: 10px; font-family: 'Bricolage Grotesque', sans-serif;
  font-weight: 800; font-size: 1.25rem; color: var(--ink); }
.nav .brand svg { width: 38px; height: 38px; }
.nav .free { padding: .28rem .8rem; border-radius: 999px; font-size: .82rem; font-weight: 700; color: #0B6B60;
  background: rgba(20, 184, 166, .16); border: 1px solid rgba(20, 184, 166, .4); }

/* ── Bandeau d'accueil ─────────────────────────────────── */
.hero {
  position: relative; overflow: hidden; border-radius: 26px; padding: 1.7rem 1.4rem 1.5rem; color: #fff;
  background:
    radial-gradient(420px 260px at 96% -14%, rgba(20, 184, 166, .5), transparent 62%),
    linear-gradient(125deg, #0D1033 0%, #2B2A8F 46%, #6D4AE8 100%);
  background-size: 100% 100%, 230% 230%;
  animation: aurora 16s ease-in-out infinite alternate;
  box-shadow: 0 30px 56px -30px rgba(13, 16, 51, .8), inset 0 1px 0 rgba(255, 255, 255, .18);
}
@keyframes aurora { from { background-position: 0 0, 0% 50%; } to { background-position: 0 0, 100% 50%; } }
.hero h1 { margin: 0; padding-right: 92px; font-size: 1.85rem; font-weight: 800; line-height: 1.12; color: #fff !important; }
.hero p { margin: .8rem 0 0; padding-right: 30px; max-width: 46ch; color: rgba(255, 255, 255, .86); font-size: 1.02rem; line-height: 1.55; }
.hero .cta {
  display: inline-block; margin-top: 1.15rem; padding: .78rem 1.35rem; border-radius: 14px; font-weight: 700;
  color: #2B2A8F !important; background: #fff; text-decoration: none; box-shadow: 0 14px 26px -14px rgba(0, 0, 0, .6);
  transition: transform .15s ease, box-shadow .15s ease;
}
.hero .cta:hover { transform: translateY(-2px); box-shadow: 0 18px 30px -14px rgba(0, 0, 0, .7); }
.pills { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: 1.1rem; }
.pills span { padding: .3rem .75rem; border-radius: 999px; font-size: .82rem; color: #fff;
  background: rgba(255, 255, 255, .13); border: 1px solid rgba(255, 255, 255, .25);
  backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }
.hero-doc { position: absolute; top: 22px; right: 16px; width: 72px; padding: 10px 8px 11px; border-radius: 10px;
  background: #fff; transform: rotate(7deg); box-shadow: 0 18px 30px -12px rgba(0, 0, 0, .55); }
.hero-doc i { display: block; height: 5px; margin-top: 6px; border-radius: 3px; background: #E3E6F8; }
.hero-doc i.n { height: 8px; width: 62%; margin-top: 0; background: var(--indigo); }
.hero-doc i.a { height: 3px; width: 34%; background: var(--sun); }
.hero-doc b { position: absolute; right: -9px; bottom: -9px; width: 26px; height: 26px; display: grid; place-items: center;
  border-radius: 50%; background: var(--sun); color: var(--ink); border: 3px solid #fff; font-size: .72rem; }
@media (min-width: 700px) {
  .hero { padding: 2.3rem 2.2rem 2rem; }
  .hero h1 { font-size: 2.9rem; padding-right: 170px; }
  .hero p { font-size: 1.12rem; padding-right: 150px; }
  .hero-doc { width: 122px; right: 34px; top: 34px; padding: 15px 13px 16px; }
}

/* ── Les 3 étapes ──────────────────────────────────────── */
.how { display: grid; grid-template-columns: repeat(3, 1fr); gap: .6rem; margin: 1rem 0 .4rem; }
.how .step { padding: .8rem .85rem; border-radius: 16px; background: #fff; border: 1px solid var(--line); color: var(--muted); }
.how .num { width: 26px; height: 26px; display: grid; place-items: center; margin-bottom: .4rem; border-radius: 50%;
  font-size: .8rem; font-weight: 700; background: #E9ECFA; color: var(--muted); }
.how b { display: block; font-family: 'Bricolage Grotesque', sans-serif; font-size: .98rem; color: var(--ink); }
.how span.txt { display: none; font-size: .88rem; line-height: 1.4; }
.how .active { border-color: var(--indigo); box-shadow: 0 16px 30px -22px rgba(79, 70, 229, .9); }
.how .active .num { color: #fff; background: linear-gradient(135deg, var(--indigo), var(--orchid)); box-shadow: 0 0 0 4px rgba(139, 92, 246, .2); }
.how .done .num { color: #fff; background: var(--lagoon); }
@media (min-width: 700px) { .how span.txt { display: block; margin-top: .25rem; } }

/* ── Titres et encadrés ────────────────────────────────── */
.sect { display: flex; align-items: center; gap: .6rem; margin: 1.1rem 0 .3rem;
  font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 1.1rem; color: var(--ink); }
.sect .ico { width: 34px; height: 34px; display: grid; place-items: center; border-radius: 11px; font-size: 1.05rem;
  background: linear-gradient(135deg, rgba(79, 70, 229, .14), rgba(20, 184, 166, .22)); }
.help { margin: 0 0 .5rem; color: var(--muted); font-size: .92rem; line-height: 1.5; }
.ai-box { margin: 1.3rem 0 .6rem; padding: 1.05rem 1.1rem; border-radius: 18px; border: 2px solid transparent;
  background: linear-gradient(#FBFAFF, #FBFAFF) padding-box, linear-gradient(135deg, var(--indigo), var(--orchid), var(--lagoon)) border-box; }
.ai-box strong { display: block; margin-bottom: .25rem; font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.12rem; }
.ai-box span { color: var(--muted); font-size: .92rem; line-height: 1.5; }
.ready { display: flex; align-items: center; gap: .85rem; margin: .4rem 0 .9rem; padding: .95rem 1.05rem; border-radius: 18px;
  border: 1px solid rgba(20, 184, 166, .4); background: linear-gradient(135deg, rgba(20, 184, 166, .14), rgba(139, 92, 246, .14)); }
.ready .tick { width: 38px; height: 38px; flex: none; display: grid; place-items: center; border-radius: 50%; color: #fff; font-weight: 800;
  background: linear-gradient(135deg, var(--lagoon), var(--indigo)); box-shadow: 0 8px 16px -8px rgba(79, 70, 229, .9); }
.ready strong { display: block; font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.1rem; }
.ready span:not(.tick) { color: var(--muted); font-size: .9rem; }

/* ── Formulaire ────────────────────────────────────────── */
[data-testid="stForm"] { position: relative; overflow: hidden; background: #fff; border: 1px solid var(--line); border-radius: 24px;
  padding: 1.7rem 1.3rem 1.2rem; box-shadow: 0 1px 2px rgba(20, 26, 60, .04), 0 30px 50px -34px rgba(79, 70, 229, .55); }
[data-testid="stForm"]::before { content: ""; position: absolute; inset: 0 0 auto 0; height: 4px;
  background: linear-gradient(90deg, var(--indigo), var(--orchid), var(--lagoon)); }
[data-testid="stWidgetLabel"] p { font-weight: 600; color: #262D57; }
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {
  border-radius: 12px !important; background: #F8F9FE !important; border-color: var(--line) !important; transition: border-color .15s, box-shadow .15s; }
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea { background: transparent !important; }
[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within, [data-baseweb="select"] > div:focus-within {
  border-color: var(--orchid) !important; box-shadow: 0 0 0 3px rgba(139, 92, 246, .22); }
[data-baseweb="tag"] { background: linear-gradient(135deg, var(--indigo), var(--orchid)) !important; border-radius: 999px !important; }
[data-baseweb="tag"] span { color: #fff !important; }
div[role="radiogroup"] { gap: .5rem; flex-wrap: wrap; }
label[data-baseweb="radio"] { margin: 0; padding: .38rem .95rem .38rem .65rem; cursor: pointer; background: #fff;
  border: 1.5px solid var(--line); border-radius: 999px; transition: border-color .15s, background .15s, box-shadow .15s; }
label[data-baseweb="radio"]:hover { border-color: var(--orchid); }
label[data-baseweb="radio"]:has(input:checked) { border-color: var(--indigo);
  background: linear-gradient(135deg, rgba(79, 70, 229, .1), rgba(139, 92, 246, .18)); box-shadow: 0 6px 14px -8px rgba(79, 70, 229, .8); }
label[data-baseweb="radio"] p { font-weight: 600; }
[data-testid="stExpander"] { border-radius: 16px; border: 1px solid var(--line); background: #fff; }

/* ── Boutons ───────────────────────────────────────────── */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button, .stLinkButton a {
  border-radius: 14px; font-weight: 700; padding: .7rem 1.1rem; border: 1.5px solid var(--line);
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease; }
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
  transform: translateY(-1px); border-color: var(--orchid); box-shadow: 0 12px 22px -14px rgba(79, 70, 229, .8); }
button[kind="primary"], button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] {
  color: #fff !important; border: none !important; background: linear-gradient(135deg, #4F46E5 0%, #8B5CF6 100%) !important;
  box-shadow: 0 14px 26px -14px rgba(79, 70, 229, .95); }
button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover, button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
  filter: brightness(1.06); box-shadow: 0 18px 30px -14px rgba(79, 70, 229, 1); }
button:active { transform: translateY(0) scale(.99); }
button:focus-visible, a:focus-visible { outline: 3px solid var(--sun) !important; outline-offset: 2px; }
.stFormSubmitButton > button { width: 100%; padding: .9rem 1.1rem; font-size: 1.05rem; }
.stButton, .stDownloadButton, .stLinkButton, [data-testid="stPopover"] { width: 100%; }
.stButton > button, .stDownloadButton > button, .stLinkButton a, [data-testid="stPopover"] button { width: 100%; }

/* Menu et don : deux boutons côte à côte, même sur téléphone */
[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) { flex-wrap: nowrap !important; gap: .6rem; margin: 1rem 0 .4rem; }
[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > [data-testid="stColumn"],
[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > [data-testid="column"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
[data-testid="stPopover"] button { border-radius: 14px !important; font-weight: 800 !important; padding: .7rem 1rem; }
[data-testid="stPopover"] button p { font-weight: 800 !important; }
[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:nth-child(1) button {
  color: #fff !important; border: none !important; background: linear-gradient(135deg, #4F46E5, #8B5CF6) !important;
  box-shadow: 0 14px 26px -14px rgba(79, 70, 229, .95); }
[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:nth-child(1) button p { color: #fff !important; }
[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:nth-child(2) button {
  color: #1B1440 !important; border: none !important; background: linear-gradient(135deg, #FFB84D, #FFD36E) !important;
  animation: donate-pulse 2.6s ease-in-out infinite; }
[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:nth-child(2) button p { color: #1B1440 !important; }
@keyframes donate-pulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(255, 184, 77, .55); } 50% { box-shadow: 0 0 0 9px rgba(255, 184, 77, 0); } }

/* ── Divers ────────────────────────────────────────────── */
.stTextArea textarea { line-height: 1.55; }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 16px; }
[data-testid="stAlert"] { border-radius: 14px; }
div[role="dialog"] { border-radius: 22px; }
[data-testid="stMetric"] { background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: .6rem .8rem; }
[data-testid="stMetricValue"] { font-family: 'Bricolage Grotesque', sans-serif; color: var(--indigo); }
.result-meta { color: var(--muted); font-size: .92rem; margin: -.2rem 0 .6rem; }
.foot { margin-top: 2.2rem; padding: 1.4rem 1.2rem; border-radius: 22px; text-align: center; color: rgba(255, 255, 255, .8);
  background: linear-gradient(125deg, #0D1033, #2B2A8F); font-size: .9rem; line-height: 1.6; }
.foot strong { display: block; margin-bottom: .3rem; color: #fff; font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.15rem; }

@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important; } }
</style>
"""
