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
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=DM+Sans:wght@400;500;700&display=swap');

:root {
  --ink: #12272B;
  --teal: #0E6B6B;
  --amber: #F2A93B;
  --paper: #F5F7F8;
  --line: #DCE3E5;
  --muted: #5B6B70;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
  font-family: 'DM Sans', sans-serif;
  color: var(--ink);
}
.stApp { background: var(--paper); }
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 820px; padding-top: 2.2rem; padding-bottom: 4rem; }

h1, h2, h3, h4, h5 {
  font-family: 'Bricolage Grotesque', sans-serif;
  letter-spacing: -0.01em;
  color: var(--ink);
}

/* En-tête de marque */
.brand { display: flex; align-items: center; gap: 16px; margin: 0 0 1.6rem; }
.brand svg { width: 58px; height: 58px; flex: none; }
.brand h1 { font-size: 2rem; line-height: 1.1; margin: 0; padding: 0; }
.brand p { margin: .25rem 0 0; color: var(--muted); font-size: 1rem; }

/* Formulaire */
[data-testid="stForm"] {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 1.5rem 1.5rem 1.1rem;
}
[data-testid="stForm"] h5 { margin: .4rem 0 .2rem; font-size: 1.05rem; }
.stTextInput input, .stTextArea textarea { border-radius: 10px; }
[data-baseweb="select"] > div { border-radius: 10px; }

/* Boutons */
.stFormSubmitButton button, .stButton button, .stDownloadButton button {
  border-radius: 10px;
  font-weight: 700;
  padding: .65rem 1rem;
}
.stFormSubmitButton button { width: 100%; }
.stButton, .stDownloadButton, .stLinkButton, [data-testid="stPopover"] { width: 100%; }
.stButton button, .stDownloadButton button, .stLinkButton a, [data-testid="stPopover"] button { width: 100%; }

/* Barre latérale */
[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid var(--line); }
.tip { color: var(--muted); font-size: .92rem; line-height: 1.5; }

/* Résultat */
.result-meta { color: var(--muted); font-size: .92rem; margin: -.2rem 0 .6rem; }

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
</style>
"""
