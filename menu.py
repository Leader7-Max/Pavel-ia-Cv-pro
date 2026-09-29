"""Menu déroulant (recommander, réglages, aide) et bouton de soutien."""

import streamlit as st

from helpers import bump_stat, get_secret, load_stats
from support import render_support


def _like() -> None:
    bump_stat("likes")
    st.session_state["user_has_liked"] = True


def render_menu():
    """Affiche « Menu » et « Soutenir ». Renvoie (clé API, liberté de l'IA)."""
    api_key = get_secret("GEMINI_API_KEY")
    stats = load_stats()
    left, right = st.columns(2)

    with left:
        with st.popover("☰ Menu"):
            st.markdown("### ❤️ Recommander")
            st.caption("Vous aimez cet outil ? Dites-le avec un clic.")
            if st.session_state.get("user_has_liked"):
                st.success(f"Merci beaucoup ! {stats['likes']} personne(s) recommandent l'outil.")
            else:
                st.button(f"❤️ J'aime cet outil ({stats['likes']})", on_click=_like, key="like_btn")
            st.metric("Documents créés", stats["generations"])

            st.markdown("### ⚙️ Réglages")
            if not api_key:
                api_key = st.text_input(
                    "Clé Gemini (la clé de l'IA)",
                    type="password",
                    key="api_key_input",
                    help="Clé gratuite sur https://aistudio.google.com/",
                ).strip()
            creativity = st.slider(
                "Liberté de l'IA",
                0.0, 1.0, 0.6, 0.1,
                key="creativity",
                help="Petit chiffre : texte simple et sûr. Grand chiffre : texte plus libre.",
            )

            st.markdown("### 💡 Conseils")
            st.caption(
                "Donnez des faits précis : des chiffres, des outils, des résultats. "
                "Collez l'annonce complète pour que l'IA reprenne ses mots importants."
            )

    with right:
        with st.popover("💛 Soutenir"):
            st.markdown("**Merci pour votre soutien !**")
            st.caption("Pavel IA CV est gratuit. Un petit don aide à le faire grandir.")
            render_support()

    return api_key, creativity
  
