"""Pavel IA CV — créez votre CV et votre lettre de motivation avec l'IA."""

import streamlit as st

# set_page_config doit être la toute première commande Streamlit.
st.set_page_config(
    page_title="Pavel IA CV",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from ai import build_prompts, stream_document  # noqa: E402
from form import render_form  # noqa: E402
from helpers import bump_stat, clean_output, friendly_error  # noqa: E402
from menu import render_menu  # noqa: E402
from results import render_results  # noqa: E402
from styles import CSS  # noqa: E402
from ui import footer_html, hero_html, how_html, navbar_html, section_html  # noqa: E402

st.markdown(CSS, unsafe_allow_html=True)

# ── Haut de page : barre, accueil, menu ───────────────────────
st.markdown(navbar_html(), unsafe_allow_html=True)
st.markdown(hero_html(), unsafe_allow_html=True)
api_key, creativity = render_menu()
steps_slot = st.empty()  # rempli plus bas, quand on connaît l'étape en cours


def request_regeneration() -> None:
    st.session_state["regen"] = True


# ── Formulaire ────────────────────────────────────────────────
params = render_form()
if params is None and st.session_state.pop("regen", False):
    params = st.session_state.get("params")

# ── Étape en cours ────────────────────────────────────────────
if params and api_key:
    step = 2
elif st.session_state.get("result_text"):
    step = 3
else:
    step = 1
steps_slot.markdown(how_html(step), unsafe_allow_html=True)

# ── Écriture par l'IA ─────────────────────────────────────────
if params:
    if not api_key:
        st.error("Il manque la clé de l'IA. Ouvrez « ☰ Menu », puis « Réglages », et collez la clé Gemini.")
    else:
        st.session_state["params"] = params
        system_prompt, user_prompt = build_prompts(params)
        st.markdown(section_html("✨", "L'IA écrit votre document…"), unsafe_allow_html=True)
        try:
            with st.container(border=True):
                raw_text = st.write_stream(
                    stream_document(api_key, system_prompt, user_prompt, creativity)
                )
        except Exception as err:  # noqa: BLE001
            st.error(friendly_error(err))
        else:
            st.session_state["result_text"] = clean_output(raw_text or "")
            st.session_state["gen_id"] = st.session_state.get("gen_id", 0) + 1
            bump_stat("generations")
            st.rerun()

# ── Résultat ──────────────────────────────────────────────────
if not params and st.session_state.get("result_text"):
    render_results(st.session_state["params"], request_regeneration)

st.markdown(footer_html(), unsafe_allow_html=True)
