"""Soutien au projet : bouton PayPal avec logo et fenêtre de remerciement après un téléchargement."""

import random

import streamlit as st

from helpers import get_secret

PAYPAL_URL = "https://www.paypal.me/Pavelia38"

# Chance (0 à 1) d'afficher la fenêtre après un téléchargement, et maximum par visite.
POPUP_PROBABILITY = 0.35
MAX_POPUPS_PER_SESSION = 2

PAYPAL_LOGO = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="22" height="22" '
    'role="img" aria-label="PayPal">'
    '<path fill="#003087" d="M7.076 21.337H2.47a.641.641 0 0 1-.633-.74L4.944.901C5.026.382 '
    "5.474 0 5.998 0h7.46c2.57 0 4.578.543 5.69 1.81 1.01 1.15 1.304 2.42 1.012 4.287-.023.143"
    "-.047.288-.077.437-.983 5.05-4.349 6.797-8.647 6.797h-2.19c-.524 0-.968.382-1.05.9l-1.12 "
    '7.106z"/>'
    '<path fill="#009cde" d="M21.222 6.917a3.35 3.35 0 0 0-.607-.541c-.013.076-.026.175-.041.254'
    "-.93 4.778-4.005 7.201-9.138 7.201h-2.19a.563.563 0 0 0-.556.479l-1.187 7.527h-.506l-.24 "
    "1.516a.56.56 0 0 0 .554.647h3.882c.46 0 .85-.334.922-.788.06-.26.76-4.852.816-5.09a.932."
    "932 0 0 1 .923-.788h.58c3.76 0 6.705-1.528 7.565-5.946.36-1.847.174-3.388-.777-4.471z"
    '"/></svg>'
)


def paypal_button() -> None:
    """Bouton PayPal jaune avec le logo, qui s'ouvre dans un nouvel onglet."""
    st.markdown(
        f'<a href="{PAYPAL_URL}" target="_blank" rel="noopener noreferrer" '
        'style="display:flex;align-items:center;justify-content:center;gap:10px;'
        "background:#FFC439;color:#111;font-weight:700;text-decoration:none;"
        'padding:.65rem 1rem;border-radius:10px;">'
        f"{PAYPAL_LOGO}<span>Faire un don avec PayPal</span></a>",
        unsafe_allow_html=True,
    )


def render_support() -> None:
    """Contenu commun : bouton PayPal et, si configuré, l'IBAN (dans les secrets Streamlit)."""
    paypal_button()
    iban = get_secret("IBAN")
    if iban:
        st.write("")
        st.markdown("**🏦 Virement bancaire**")
        st.markdown(f"**IBAN :** `{iban}`")


def _dialog_body() -> None:
    st.markdown("**Ce document vous a été utile ?**")
    st.write(
        "Pavel IA CV est gratuit. Si l'outil vous a fait gagner du temps, "
        "un petit don aide à le faire évoluer. Merci d'avance !"
    )
    render_support()
    st.write("")
    if st.button("Non merci, fermer"):
        st.rerun()


_dialog = getattr(st, "dialog", None) or getattr(st, "experimental_dialog", None)
support_dialog = _dialog("💛 Merci d'utiliser Pavel IA CV")(_dialog_body) if _dialog else None


def on_download() -> None:
    """À brancher sur on_click des boutons de téléchargement : décide si la fenêtre s'affiche."""
    ss = st.session_state
    ss["downloads"] = ss.get("downloads", 0) + 1
    shown = ss.get("support_shown", 0)
    if shown < MAX_POPUPS_PER_SESSION and random.random() < POPUP_PROBABILITY:
        ss["show_support"] = True
        ss["support_shown"] = shown + 1


def maybe_show_support() -> None:
    """À appeler après les boutons de téléchargement : ouvre la fenêtre si elle a été demandée."""
    if st.session_state.pop("show_support", False):
        if support_dialog:
            support_dialog()
        else:
            st.toast("Pavel IA CV est gratuit : un petit don PayPal est le bienvenu 💛")
          
