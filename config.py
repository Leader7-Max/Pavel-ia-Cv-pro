"""Constantes et styles de Pavel IA CV."""

MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-3.5-flash-lite"]  # essayés dans l'ordre : les suivants servent de secours

TONES = [
    "Professionnel et formel (classique)",
    "Dynamique et moderne (impactant)",
    "Reconversion / profil atypique",
    "Audacieux et créatif",
]

LENGTHS = {
    "cv": {
        "Concise": "tient sur une page, 3 puces maximum par expérience",
        "Standard": "tient sur une page, 3 à 4 puces par expérience",
        "Détaillée": "peut occuper deux pages, 4 à 6 puces par expérience",
    },
    "lettre": {
        "Concise": "200 à 250 mots",
        "Standard": "300 à 350 mots",
        "Détaillée": "400 à 450 mots",
    },
}

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Logo Pavel IA CV"><rect width="64" height="64" rx="16" fill="#0E6B6B"/><path d="M18 12h18l10 10v26a3 3 0 0 1-3 3H18a3 3 0 0 1-3-3V15a3 3 0 0 1 3-3z" fill="#FFFFFF"/><path d="M36 12v7a3 3 0 0 0 3 3h7z" fill="#B7D6D6"/><rect x="21" y="27" width="16" height="3" rx="1.5" fill="#0E6B6B"/><rect x="21" y="34" width="11" height="3" rx="1.5" fill="#9CC3C3"/><circle cx="44" cy="44" r="10" fill="#F2A93B" stroke="#0E6B6B" stroke-width="3"/><path d="M39.5 44.5l3.3 3.3 6-6.6" fill="none" stroke="#12272B" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:wght@400;500;700&display=swap');

:root {
  --abyss: #062B33;
  --lagoon: #0E6B6B;
  --emerald: #14A38B;
  --amber: #F2A93B;
  --sun: #FFC94D;
  --mist: #F3F7F8;
  --ink: #0F2A30;
  --line: #D7E5E7;
  --muted: #5B6F74;
}

html, body, .stApp, [data-testid="stAppViewContainer"], .stMarkdown, label, input, textarea, button {
  font-family: 'DM Sans', sans-serif;
}
.stApp {
  color: var(--ink);
  background:
    radial-gradient(900px 480px at 105% -8%, rgba(20, 163, 139, .18), transparent 60%),
    radial-gradient(760px 420px at -12% 4%, rgba(255, 201, 77, .16), transparent 55%),
    var(--mist);
  background-attachment: fixed;
}
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 820px; padding: 2.6rem 1.1rem 4rem; }
@media (max-width: 640px) { .block-container { padding-top: 3.4rem; } }

h1, h2, h3, h4, h5 {
  font-family: 'Bricolage Grotesque', sans-serif;
  letter-spacing: -0.015em;
  color: var(--ink);
}

/* ── Bandeau d'accueil ─────────────────────────────────── */
.hero {
  position: relative;
  overflow: hidden;
  border-radius: 24px;
  padding: 1.5rem 1.35rem 1.35rem;
  color: #fff;
  background:
    radial-gradient(420px 260px at 96% -12%, rgba(110, 245, 220, .34), transparent 62%),
    linear-gradient(120deg, #062B33 0%, #0E6B6B 52%, #14A38B 100%);
  background-size: 100% 100%, 220% 220%;
  animation: aurora 16s ease-in-out infinite alternate;
  box-shadow: 0 24px 48px -26px rgba(6, 43, 51, .7), inset 0 1px 0 rgba(255, 255, 255, .18);
}
@keyframes aurora {
  from { background-position: 0 0, 0% 50%; }
  to { background-position: 0 0, 100% 50%; }
}
.hero-head { display: flex; align-items: center; gap: 12px; padding-right: 88px; }
.hero-head svg { width: 46px; height: 46px; flex: none; }
.hero .hero-head h1 {
  font-size: 1.7rem; font-weight: 800; line-height: 1.05; margin: 0; padding: 0; color: #fff !important;
  white-space: nowrap;
}
.hero .hero-sub {
  margin: .85rem 0 0; padding-right: 88px; max-width: 46ch;
  color: rgba(255, 255, 255, .86); font-size: 1rem; line-height: 1.5;
}
.pills { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: 1.05rem; }
.pills span {
  padding: .3rem .75rem; border-radius: 999px; font-size: .82rem; font-weight: 500; color: #fff;
  background: rgba(255, 255, 255, .13); border: 1px solid rgba(255, 255, 255, .24);
  backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
}
.hero-doc {
  position: absolute; top: 20px; right: 16px; width: 76px; padding: 10px 8px 11px;
  border-radius: 10px; background: #fff; transform: rotate(6deg);
  box-shadow: 0 18px 30px -12px rgba(0, 0, 0, .5);
}
.hero-doc i { display: block; height: 5px; margin-top: 6px; border-radius: 3px; background: #DCE8EA; }
.hero-doc i.n { height: 8px; width: 62%; margin-top: 0; background: var(--lagoon); }
.hero-doc i.a { height: 3px; width: 34%; background: var(--amber); }
.hero-doc b {
  position: absolute; right: -9px; bottom: -9px; width: 26px; height: 26px; display: grid;
  place-items: center; border-radius: 50%; background: var(--amber); color: var(--ink);
  border: 3px solid #fff; font-size: .72rem;
}
@media (min-width: 700px) {
  .hero { padding: 1.9rem 1.9rem 1.7rem; }
  .hero-doc { width: 122px; right: 30px; top: 26px; padding: 15px 13px 16px; }
  .hero-head, .hero .hero-sub { padding-right: 160px; }
  .hero-head svg { width: 54px; height: 54px; }
  .hero .hero-head h1 { font-size: 2.5rem; }
}

/* ── Étapes ────────────────────────────────────────────── */
.stepper { display: flex; align-items: center; gap: .55rem; margin: 1.1rem .2rem 1.2rem; }
.step { display: flex; align-items: center; gap: .5rem; font-size: .88rem; font-weight: 600; color: var(--muted); }
.step .dot {
  width: 26px; height: 26px; flex: none; display: grid; place-items: center; border-radius: 50%;
  font-size: .8rem; font-weight: 700; background: #E1ECEE; color: var(--muted);
  transition: background .3s, box-shadow .3s;
}
.step.active { color: var(--ink); }
.step.active .dot {
  color: #fff; background: linear-gradient(135deg, var(--lagoon), var(--emerald));
  box-shadow: 0 0 0 4px rgba(20, 163, 139, .2);
}
.step.done { color: var(--lagoon); }
.step.done .dot { color: #fff; background: var(--lagoon); }
.stepper .bar { flex: 1; min-width: 10px; height: 2px; border-radius: 2px; background: #D9E6E8; }
.stepper .bar.done { background: linear-gradient(90deg, var(--lagoon), var(--emerald)); }
@media (max-width: 520px) {
  .step .lbl { display: none; }
  .step.active .lbl { display: inline; }
}

/* ── Formulaire ────────────────────────────────────────── */
[data-testid="stForm"] {
  position: relative; overflow: hidden; background: #fff; border: 1px solid var(--line);
  border-radius: 22px; padding: 1.7rem 1.4rem 1.2rem;
  box-shadow: 0 1px 2px rgba(15, 42, 48, .04), 0 26px 46px -30px rgba(14, 107, 107, .45);
}
[data-testid="stForm"]::before {
  content: ""; position: absolute; inset: 0 0 auto 0; height: 4px;
  background: linear-gradient(90deg, var(--lagoon), var(--emerald), var(--sun));
}
.sect { display: flex; align-items: center; gap: .6rem; margin: 1rem 0 .35rem;
  font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 1.08rem; color: var(--ink); }
.sect .ico {
  width: 32px; height: 32px; display: grid; place-items: center; border-radius: 10px; font-size: 1rem;
  background: linear-gradient(135deg, rgba(14, 107, 107, .13), rgba(255, 201, 77, .3));
}
[data-testid="stWidgetLabel"] p { font-weight: 600; color: #1B3A40; }

[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {
  border-radius: 12px !important; background: #F7FBFB !important; border-color: var(--line) !important;
  transition: border-color .15s, box-shadow .15s;
}
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea { background: transparent !important; }
[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within,
[data-baseweb="select"] > div:focus-within {
  border-color: var(--emerald) !important; box-shadow: 0 0 0 3px rgba(20, 163, 139, .2);
}

/* Choix par pastilles (type de document, modèle) */
div[role="radiogroup"] { gap: .5rem; flex-wrap: wrap; }
label[data-baseweb="radio"] {
  margin: 0; padding: .38rem .95rem .38rem .65rem; cursor: pointer; background: #fff;
  border: 1.5px solid var(--line); border-radius: 999px;
  transition: border-color .15s, background .15s, box-shadow .15s;
}
label[data-baseweb="radio"]:hover { border-color: var(--emerald); }
label[data-baseweb="radio"]:has(input:checked) {
  border-color: var(--lagoon);
  background: linear-gradient(135deg, rgba(14, 107, 107, .1), rgba(20, 163, 139, .18));
  box-shadow: 0 6px 14px -8px rgba(14, 107, 107, .8);
}
label[data-baseweb="radio"] p { font-weight: 600; }

/* ── Boutons ───────────────────────────────────────────── */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button, .stLinkButton a {
  border-radius: 14px; font-weight: 700; padding: .7rem 1.1rem; border: 1.5px solid var(--line);
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
  transform: translateY(-1px); border-color: var(--emerald); box-shadow: 0 10px 20px -12px rgba(14, 107, 107, .7);
}
button[kind="primary"], button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] {
  color: #fff !important; border: none !important;
  background: linear-gradient(135deg, #0E6B6B 0%, #14A38B 100%) !important;
  box-shadow: 0 12px 24px -12px rgba(14, 107, 107, .85);
}
button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
  box-shadow: 0 16px 28px -12px rgba(14, 107, 107, .95); filter: brightness(1.05);
}
button:active { transform: translateY(0) scale(.99); }
button:focus-visible, a:focus-visible { outline: 3px solid var(--sun) !important; outline-offset: 2px; }
.stFormSubmitButton > button { width: 100%; padding: .85rem 1.1rem; font-size: 1.02rem; }
.stButton, .stDownloadButton, .stLinkButton, [data-testid="stPopover"] { width: 100%; }
.stButton > button, .stDownloadButton > button, .stLinkButton a, [data-testid="stPopover"] > div > button { width: 100%; }

/* Bouton de don : dégradé ambre et halo discret */
[data-testid="stPopover"] button, [data-testid="stPopoverButton"] {
  background: linear-gradient(135deg, #F2A93B 0%, #FFC94D 100%) !important;
  color: #12272B !important; border: none !important; font-weight: 800 !important;
  border-radius: 14px !important; animation: donate-pulse 2.6s ease-in-out infinite;
}
[data-testid="stPopover"] button p, [data-testid="stPopoverButton"] p { color: #12272B !important; font-weight: 800 !important; }
@keyframes donate-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(242, 169, 59, .5); }
  50% { box-shadow: 0 0 0 9px rgba(242, 169, 59, 0); }
}

/* ── Résultat ──────────────────────────────────────────── */
.ready {
  display: flex; align-items: center; gap: .85rem; margin: .4rem 0 .9rem; padding: .95rem 1.05rem;
  border-radius: 18px; border: 1px solid rgba(20, 163, 139, .32);
  background: linear-gradient(135deg, rgba(20, 163, 139, .13), rgba(255, 201, 77, .2));
}
.ready .tick {
  width: 36px; height: 36px; flex: none; display: grid; place-items: center; border-radius: 50%;
  color: #fff; font-weight: 800; background: linear-gradient(135deg, var(--lagoon), var(--emerald));
  box-shadow: 0 8px 16px -8px rgba(14, 107, 107, .9);
}
.ready strong { display: block; font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.08rem; }
.ready span:not(.tick) { color: var(--muted); font-size: .9rem; }
.result-meta { color: var(--muted); font-size: .92rem; margin: -.2rem 0 .6rem; }
.stTextArea textarea { line-height: 1.55; }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 16px; }
[data-testid="stAlert"] { border-radius: 14px; }
div[role="dialog"] { border-radius: 22px; }

/* ── Barre latérale ────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #FFFFFF 0%, #F1F8F8 100%); border-right: 1px solid var(--line);
}
[data-testid="stMetric"] {
  background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: .6rem .8rem;
}
[data-testid="stMetricValue"] { font-family: 'Bricolage Grotesque', sans-serif; color: var(--lagoon); }
.tip { color: var(--muted); font-size: .92rem; line-height: 1.5; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
</style>
"""
