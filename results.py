"""Affichage du résultat : texte modifiable, choix du style, téléchargements."""

import re

import streamlit as st

from exporters import DOCX_AVAILABLE, build_docx, build_pdf
from helpers import keyword_match, slugify
from support import maybe_show_support, on_download
from templates import TEMPLATES, preview_html
from ui import ready_html, section_html


def render_results(p: dict, on_regenerate) -> None:
    is_cv = p["doc_type"].startswith("CV")
    editor_key = f"editor_{st.session_state['gen_id']}"

    st.markdown(ready_html("CV" if is_cv else "lettre"), unsafe_allow_html=True)
    st.text_area(
        "Texte du document",
        value=st.session_state["result_text"],
        height=460,
        key=editor_key,
        label_visibility="collapsed",
    )
    final_text = st.session_state[editor_key]

    with st.expander("📋 Copier le texte"):
        st.code(final_text, language=None)

    fields = re.findall(r"\[[^\]]+\]", final_text)
    if fields:
        st.info(
            f"Il reste {len(fields)} case(s) à remplir entre crochets [ ]. "
            f"Exemple : {fields[0]}. Changez-les dans le texte ci-dessus."
        )

    st.markdown(
        section_html("🎨", "Choisissez un style", "Le style change les couleurs et la forme du document."),
        unsafe_allow_html=True,
    )
    template = st.radio(
        "Style du document", list(TEMPLATES), horizontal=True, key="template_choice",
        label_visibility="collapsed",
    )
    st.caption(TEMPLATES[template]["desc"])
    st.markdown(preview_html(template), unsafe_allow_html=True)

    st.markdown(section_html("⬇️", "Télécharger"), unsafe_allow_html=True)
    file_base = f"{'CV' if is_cv else 'Lettre_motivation'}_{slugify(p['name'])}"
    d1, d2, d3 = st.columns(3)
    with d1:
        try:
            pdf_bytes = build_pdf(final_text, is_cv, template)
        except Exception as err:  # noqa: BLE001
            pdf_bytes = None
            st.error(f"Le PDF n'a pas pu être créé : {err}")
        if pdf_bytes:
            st.download_button(
                "📄 PDF", data=pdf_bytes, file_name=f"{file_base}.pdf", mime="application/pdf",
                on_click=on_download, type="primary",
            )
    with d2:
        if DOCX_AVAILABLE:
            try:
                docx_bytes = build_docx(final_text, is_cv, template)
            except Exception as err:  # noqa: BLE001
                docx_bytes = None
                st.error(f"Le fichier Word n'a pas pu être créé : {err}")
            if docx_bytes:
                st.download_button(
                    "📝 Word", data=docx_bytes, file_name=f"{file_base}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    on_click=on_download, type="primary",
                )
        else:
            st.caption("Word n'est pas disponible : ajoutez python-docx dans requirements.txt.")
    with d3:
        st.download_button(
            "🗒️ Texte", data=final_text.encode("utf-8"), file_name=f"{file_base}.txt",
            mime="text/plain", on_click=on_download,
        )

    maybe_show_support()

    st.button("🔄 Écrire une autre version", on_click=on_regenerate, key="regen_btn")

    if p.get("offer"):
        match = keyword_match(p["offer"], final_text)
        if match:
            found, total, missing = match
            st.markdown(section_html("🔎", "Votre document et l'annonce"), unsafe_allow_html=True)
            st.progress(found / total, text=f"{found} mots importants de l'annonce sur {total} sont dans votre document")
            if missing:
                st.caption(
                    "Mots de l'annonce qui manquent (ajoutez-les seulement s'ils sont vrais pour vous) : "
                    + ", ".join(missing[:10])
                )
