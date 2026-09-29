"""Pavel IA CV — générateur de CV et lettres de motivation sur-mesure."""

import re

import streamlit as st

# set_page_config doit être la toute première commande Streamlit.
st.set_page_config(
    page_title="Pavel IA CV",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from ai import build_prompts, stream_document  # noqa: E402
from config import CSS, LENGTHS, TONES  # noqa: E402
from exporters import DOCX_AVAILABLE, build_docx, build_pdf  # noqa: E402
from support import maybe_show_support, on_download, render_support  # noqa: E402
from templates import TEMPLATES, preview_html  # noqa: E402
from ui import hero_html, ready_html, section_html, stepper_html  # noqa: E402
from helpers import (  # noqa: E402
    bump_stat,
    clean_output,
    friendly_error,
    get_secret,
    keyword_match,
    load_stats,
    slugify,
)

st.markdown(CSS, unsafe_allow_html=True)

if "user_has_liked" not in st.session_state:
    st.session_state.user_has_liked = False


# ─────────────────────────────────────────────────────────────
# Interface
# ─────────────────────────────────────────────────────────────
st.markdown(hero_html(), unsafe_allow_html=True)

# Bouton de don visible d'emblée (la barre latérale est repliée sur mobile).
with st.popover("💰 Soutenir Pavel IA CV"):
    st.markdown("**Merci pour votre soutien !**")
    render_support()

stepper_slot = st.empty()  # rempli plus bas, une fois l'état connu

with st.sidebar:
    st.markdown("### Réglages")
    api_key = get_secret("GEMINI_API_KEY")
    if not api_key:
        api_key = st.text_input(
            "Clé API Gemini",
            type="password",
            help="Clé gratuite sur https://aistudio.google.com/",
        ).strip()
    creativity = st.slider(
        "Créativité",
        0.0, 1.0, 0.6, 0.1,
        help="Bas : texte sobre et fidèle à vos données. Haut : formulations plus libres.",
    )
    st.markdown(
        '<p class="tip">Plus vous donnez de faits précis (chiffres, outils, résultats), '
        "plus le document est convaincant. Collez l'offre complète pour que les mots-clés "
        "soient repris.</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # --- SECTION STATISTIQUES (réelles) ---
    stats = load_stats()
    st.markdown("### Statistiques")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric(label="Docs créés", value=stats["generations"])
    with col_stat2:
        st.metric(label="Recommandations", value=stats["likes"])

    # --- SECTION LIKES ---
    if not st.session_state.user_has_liked:
        if st.button(f"👍 Recommander cet outil ({stats['likes']})"):
            bump_stat("likes")
            st.session_state.user_has_liked = True
            st.rerun()
    else:
        st.info(f"❤️ Merci pour votre soutien ! ({stats['likes']})")

    st.divider()

    # --- SECTION SOUTIEN / DON ---
    st.markdown("### Soutenir le projet")
    st.caption("Pavel IA CV est gratuit. Vous pouvez encourager son développement :")

    with st.popover("☕ Faire un don / Encourager"):
        st.markdown("**Merci pour votre soutien !**")
        render_support()

with st.form("cv_form"):
    doc_type = st.radio("Document à créer", ["Lettre de motivation", "CV"], horizontal=True)

    st.markdown(section_html("🎯", "Candidat et poste"), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Nom et prénom")
        job = st.text_input("Poste visé")
    with c2:
        company = st.text_input("Entreprise (facultatif pour un CV)")
        tone = st.selectbox("Ton de rédaction", TONES)

    c3, c4 = st.columns(2)
    with c3:
        language = st.selectbox("Langue du document", ["Français", "English"])
    with c4:
        length = st.selectbox("Longueur", list(LENGTHS["cv"].keys()), index=1)

    st.markdown(section_html("🧭", "Votre parcours"), unsafe_allow_html=True)
    background = st.text_area(
        "Parcours et compétences clés",
        height=160,
        max_chars=4000,
        placeholder="Ex : 3 ans en gestion de projet chez X, 12 personnes coordonnées, maîtrise d'Excel et de Jira, autonomie…",
    )

    st.markdown(section_html("📋", "Offre d'emploi"), unsafe_allow_html=True)
    offer = st.text_area(
        "Texte de l'annonce (facultatif)",
        height=140,
        max_chars=6000,
        placeholder="Collez l'annonce pour adapter le document à ses mots-clés.",
    )
    notes = st.text_area(
        "Consignes particulières (facultatif)",
        height=80,
        max_chars=1000,
        placeholder="Ex : insister sur ma disponibilité immédiate.",
    )

    submitted = st.form_submit_button("✨ Générer mon document", type="primary")


def request_regeneration():
    st.session_state["regen"] = True


params = None
if submitted:
    if not name.strip() or not job.strip() or not background.strip():
        st.warning("Renseignez au moins votre nom, le poste visé et votre parcours.")
    else:
        params = {
            "doc_type": doc_type, "name": name.strip(), "job": job.strip(),
            "company": company.strip(), "tone": tone, "language": language,
            "length": length, "background": background.strip(),
            "offer": offer.strip(), "notes": notes.strip(),
        }
if not submitted and st.session_state.pop("regen", False):
    params = st.session_state.get("params")

# Étapes (1 = informations, 2 = rédaction, 3 = téléchargement)
if params and api_key:
    step = 2
elif st.session_state.get("result_text"):
    step = 3
else:
    step = 1
stepper_slot.markdown(stepper_html(step), unsafe_allow_html=True)

# Génération
if params:
    if not api_key:
        st.error("Aucune clé API : ajoutez GEMINI_API_KEY dans les secrets ou dans la barre latérale.")
    else:
        st.session_state["params"] = params
        system_prompt, user_prompt = build_prompts(params)
        st.markdown(section_html("✨", "Rédaction en cours…"), unsafe_allow_html=True)
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

# Résultat
if not params and st.session_state.get("result_text"):
    p = st.session_state["params"]
    is_cv = p["doc_type"].startswith("CV")
    editor_key = f"editor_{st.session_state['gen_id']}"

    st.markdown(ready_html("CV" if is_cv else "lettre"), unsafe_allow_html=True)
    st.markdown(
        '<p class="result-meta">Modifiez le texte directement : les exports utilisent cette version.</p>',
        unsafe_allow_html=True,
    )
    st.text_area(
        "Texte du document",
        value=st.session_state["result_text"],
        height=460,
        key=editor_key,
        label_visibility="collapsed",
    )
    final_text = st.session_state[editor_key]

    placeholders = re.findall(r"\[[^\]]+\]", final_text)
    if placeholders:
        st.info(
            f"{len(placeholders)} champ(s) à compléter entre crochets, par exemple : "
            f"{placeholders[0]}"
        )

    file_base = f"{'CV' if is_cv else 'Lettre_motivation'}_{slugify(p['name'])}"
    st.markdown(section_html("🎨", "Modèle de mise en page"), unsafe_allow_html=True)
    template = st.radio(
        "Modèle de mise en page",
        list(TEMPLATES),
        horizontal=True,
        key="template_choice",
        label_visibility="collapsed",
    )
    st.caption(TEMPLATES[template]["desc"])
    st.markdown(preview_html(template), unsafe_allow_html=True)

    st.markdown(section_html("⬇️", "Télécharger"), unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        try:
            pdf_bytes = build_pdf(final_text, is_cv, template)
        except Exception as err:  # noqa: BLE001
            pdf_bytes = None
            st.error(f"Export PDF impossible : {err}")
        if pdf_bytes:
            st.download_button(
                "📄 PDF",
                data=pdf_bytes,
                file_name=f"{file_base}.pdf",
                mime="application/pdf",
                on_click=on_download,
                type="primary",
            )
    with d2:
        if DOCX_AVAILABLE:
            try:
                docx_bytes = build_docx(final_text, is_cv, template)
            except Exception as err:  # noqa: BLE001
                docx_bytes = None
                st.error(f"Export Word impossible : {err}")
            if docx_bytes:
                st.download_button(
                    "📝 Word (.docx)",
                    data=docx_bytes,
                    file_name=f"{file_base}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    on_click=on_download,
                    type="primary",
                )
        else:
            st.caption("Export Word indisponible : ajoutez python-docx à requirements.txt.")
    with d3:
        st.download_button(
            "🗒️ Texte (.txt)",
            data=final_text.encode("utf-8"),
            file_name=f"{file_base}.txt",
            mime="text/plain",
            on_click=on_download,
        )

    maybe_show_support()

    st.button(
        "🔄 Régénérer avec les mêmes informations",
        on_click=request_regeneration,
    )

    # Correspondance avec les mots-clés de l'offre
    if p.get("offer"):
        match = keyword_match(p["offer"], final_text)
        if match:
            found, total, missing = match
            st.markdown(section_html("🔎", "Correspondance avec l'offre"), unsafe_allow_html=True)
            st.progress(found / total, text=f"{found} mots-clés sur {total} présents dans votre document")
            if missing:
                st.caption(
                    "Mots-clés absents (à ajouter seulement s'ils correspondent à votre parcours) : "
                    + ", ".join(missing[:10])
                )
