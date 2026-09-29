"""Formulaire de création du document (mots simples, aides et exemples)."""

import streamlit as st

from config import DOC_LANGUAGES, LENGTHS, QUICK_IDEAS, TONES
from ui import ai_box_html, section_html

# Exemple rempli d'un clic pour montrer comment remplir le formulaire.
EXAMPLE = {
    "f_doc": "CV",
    "f_name": "Sara Martin",
    "f_email": "sara.martin@email.com",
    "f_phone": "+33 6 12 34 56 78",
    "f_city": "Lyon, France",
    "f_link": "",
    "f_job": "Assistante administrative",
    "f_company": "",
    "f_exp": (
        "2022 à 2024 : Réceptionniste à l'hôtel Soleil, à Lyon. J'accueillais les clients, "
        "je gérais les réservations et je répondais à environ 40 appels par jour.\n"
        "2020 à 2022 : Vendeuse dans un magasin de vêtements. Je conseillais les clients et je gérais la caisse."
    ),
    "f_edu": "2020 : Baccalauréat professionnel Métiers de l'accueil, Lyon.",
    "f_skills": "Excel, Word, accueil des clients, gestion du courrier, travail en équipe",
    "f_langs": "Français (langue maternelle), Anglais (courant), Espagnol (bases)",
    "f_strengths": "Sérieuse, organisée, à l'écoute, toujours à l'heure",
    "f_offer": "",
    "f_quick": ["Utiliser des mots très simples"],
    "f_special": "",
}


def fill_example() -> None:
    for key, value in EXAMPLE.items():
        st.session_state[key] = value


def render_form():
    """Affiche le formulaire. Renvoie un dictionnaire de choix quand on clique sur « Créer », sinon None."""
    st.header("Créer mon document", anchor="creer")
    st.caption("Remplissez ce que vous savez. Les champs « obligatoire » sont les plus importants.")

    with st.expander("💡 Besoin d'aide ? Lisez ceci"):
        st.markdown(
            "- **CV** : une page qui montre votre parcours (travail, études, compétences).\n"
            "- **Lettre de motivation** : un texte qui explique pourquoi vous voulez ce travail.\n"
            "- Vous pouvez écrire avec des phrases courtes. L'IA va les améliorer.\n"
            "- Vous ne savez pas quoi écrire ? Cliquez sur **« Voir un exemple »**.\n"
            "- Vous pourrez **changer le texte** avant de télécharger."
        )
    st.button("👀 Voir un exemple rempli", on_click=fill_example, key="example_btn")

    with st.form("cv_form"):
        doc_type = st.radio(
            "Quel document voulez-vous ?", ["CV", "Lettre de motivation"], horizontal=True, key="f_doc"
        )

        st.markdown(section_html("👤", "Qui êtes-vous ?"), unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Nom complet (obligatoire)", key="f_name", placeholder="Ex : Sara Martin")
            phone = st.text_input("Téléphone", key="f_phone", placeholder="Ex : +33 6 12 34 56 78")
            link = st.text_input("Lien LinkedIn ou site (facultatif)", key="f_link")
        with c2:
            email = st.text_input("Email", key="f_email", placeholder="Ex : sara@email.com")
            city = st.text_input("Ville et pays", key="f_city", placeholder="Ex : Lyon, France")

        st.markdown(section_html("🎯", "Quel travail voulez-vous ?"), unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            job = st.text_input(
                "Poste voulu (obligatoire)", key="f_job", placeholder="Ex : Assistante administrative"
            )
        with c4:
            company = st.text_input("Nom de l'entreprise (facultatif)", key="f_company")

        st.markdown(
            section_html("🧭", "Votre parcours", "Écrivez avec vos mots. Des phrases courtes sont très bien."),
            unsafe_allow_html=True,
        )
        background = st.text_area(
            "Vos expériences de travail (obligatoire)",
            key="f_exp",
            height=150,
            max_chars=4000,
            placeholder="Ex : 2022 à 2024, réceptionniste à l'hôtel Soleil. J'accueillais les clients et je gérais les réservations.",
            help="Pour chaque travail : le poste, l'entreprise, les dates et ce que vous avez fait.",
        )
        education = st.text_area(
            "Vos études et diplômes", key="f_edu", height=90, max_chars=1500,
            placeholder="Ex : 2020, Baccalauréat, Lyon.",
        )
        c5, c6 = st.columns(2)
        with c5:
            skills = st.text_input("Vos compétences", key="f_skills", placeholder="Ex : Excel, accueil, anglais")
        with c6:
            languages_spoken = st.text_input(
                "Langues que vous parlez", key="f_langs", placeholder="Ex : Français (courant), Anglais (bases)"
            )
        strengths = st.text_input(
            "Vos qualités", key="f_strengths", placeholder="Ex : sérieux, organisé, à l'écoute"
        )

        st.markdown(
            section_html("📋", "L'annonce du travail (facultatif)", "Copiez l'annonce ici. L'IA reprendra ses mots importants."),
            unsafe_allow_html=True,
        )
        offer = st.text_area("Texte de l'annonce", key="f_offer", height=130, max_chars=6000,
                             label_visibility="collapsed", placeholder="Collez l'annonce ici.")

        st.markdown(section_html("🎨", "Le style du document"), unsafe_allow_html=True)
        c7, c8, c9 = st.columns(3)
        with c7:
            tone = st.selectbox("Ton", TONES, key="f_tone")
        with c8:
            language = st.selectbox("Langue du document", DOC_LANGUAGES, key="f_lang")
        with c9:
            length = st.selectbox("Longueur", list(LENGTHS["cv"]), index=1, key="f_length")

        st.markdown(ai_box_html(), unsafe_allow_html=True)
        quick = st.multiselect(
            "Idées rapides (choisissez ce que vous voulez)", QUICK_IDEAS, key="f_quick"
        )
        special = st.text_area(
            "Votre ordre pour l'IA (facultatif)",
            key="f_special",
            height=110,
            max_chars=1200,
            placeholder="Ex : Écris une lettre très motivée. Parle de mon expérience à l'étranger. Garde un ton simple et poli.",
        )

        submitted = st.form_submit_button("✨ Créer mon document", type="primary")

    if not submitted:
        return None
    if not name.strip() or not job.strip() or not background.strip():
        st.warning("Écrivez au moins : votre nom, le poste voulu et vos expériences de travail.")
        return None
    return {
        "doc_type": doc_type, "name": name.strip(), "email": email.strip(), "phone": phone.strip(),
        "city": city.strip(), "link": link.strip(), "job": job.strip(), "company": company.strip(),
        "background": background.strip(), "education": education.strip(), "skills": skills.strip(),
        "languages_spoken": languages_spoken.strip(), "strengths": strengths.strip(),
        "offer": offer.strip(), "tone": tone, "language": language, "length": length,
        "quick": list(quick), "special": special.strip(),
          }
                                    
