"""Pavel IA CV — moteur IA Gemini pour CV, lettres et candidatures."""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import Any

from google import genai
from google.genai import types


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_MODEL = "gemini-3.8-flash"

SUPPORTED_LANGUAGES = {
    "Français": "français",
    "English": "anglais",
    "Deutsch": "allemand",
    "Español": "espagnol",
    "Italiano": "italien",
}

CV_FORMATS = {
    "CV classique": "sobre, professionnel, clair et chronologique",
    "CV moderne": "moderne, dynamique, lisible et professionnel",
    "CV premium": "haut de gamme, élégant, structuré et professionnel",
    "CV ATS": "optimisé pour les logiciels ATS et facile à analyser",
    "CV européen": "adapté aux usages professionnels européens",
    "CV international": "adapté à une candidature internationale",
    "CV étudiant": "adapté à un étudiant ou à un profil débutant",
    "CV sans expérience": "valorisant les compétences transférables",
    "CV reconversion": "mettant en avant les compétences transférables",
}


# ============================================================
# UTILITAIRES
# ============================================================

def _clean(value: Any, maximum: int | None = None) -> str:
    """Nettoie une valeur utilisateur."""
    if value is None:
        return ""

    text = str(value).strip()

    if maximum is not None:
        text = text[:maximum]

    return text


def _language_name(language: str) -> str:
    """Retourne le nom complet de la langue."""
    return SUPPORTED_LANGUAGES.get(language, language or "français")


# ============================================================
# INSTRUCTIONS DOCUMENT
# ============================================================

def _document_instruction(params: dict[str, Any]) -> str:
    """Construit les instructions propres au type de document."""

    doc_type = _clean(params.get("doc_type"))
    job = _clean(params.get("job"))
    company = _clean(params.get("company"))
    language = _language_name(_clean(params.get("language")))
    length = _clean(params.get("length"))
    tone = _clean(params.get("tone"))

    if doc_type.lower().startswith("cv"):
        format_hint = CV_FORMATS.get(
            doc_type,
            "professionnel, moderne et parfaitement lisible",
        )

        return f"""
TYPE DE DOCUMENT : CV

POSTE VISÉ :
{job}

ENTREPRISE :
{company or "Non précisée"}

LANGUE :
{language}

LONGUEUR :
{length or "Équilibrée"}

TON :
{tone or "Professionnel"}

STYLE :
{format_hint}

OBJECTIF :

Créer un CV professionnel directement utilisable pour une candidature.

Le CV doit :

- avoir un titre professionnel précis ;
- contenir un profil professionnel clair ;
- présenter les expériences de manière structurée ;
- mettre en valeur les compétences réellement fournies ;
- utiliser des verbes d'action ;
- être facile à lire ;
- être compatible avec une lecture humaine ;
- être compatible avec une lecture ATS ;
- reprendre naturellement les mots-clés pertinents de l'offre ;
- ne jamais inventer une information.

Ne jamais inventer :

- expérience ;
- entreprise ;
- diplôme ;
- certification ;
- date ;
- compétence ;
- responsabilité ;
- chiffre ;
- résultat.
"""

    return f"""
TYPE DE DOCUMENT : LETTRE DE MOTIVATION

POSTE VISÉ :
{job}

ENTREPRISE :
{company or "Non précisée"}

LANGUE :
{language}

LONGUEUR :
{length or "Équilibrée"}

TON :
{tone or "Professionnel"}

OBJECTIF :

Rédiger une lettre de motivation personnalisée, naturelle et crédible.

La lettre doit :

- commencer par une accroche naturelle ;
- montrer l'intérêt pour le poste ;
- mettre en valeur les compétences réellement fournies ;
- utiliser les éléments pertinents de l'offre ;
- expliquer la motivation ;
- rester humaine ;
- éviter les phrases génériques ;
- ne jamais inventer une information.
"""


# ============================================================
# PROMPT SYSTÈME
# ============================================================

def _global_system_prompt() -> str:
    """Instruction principale de Pavel IA."""

    return """
Tu es Pavel IA, un assistant professionnel spécialisé dans :

- les CV ;
- les lettres de motivation ;
- les candidatures ;
- l'analyse d'offres d'emploi ;
- l'amélioration de profils professionnels.

MISSION :

Transformer les informations fournies par le candidat en documents
professionnels, crédibles, clairs et directement exploitables.

RÈGLE ABSOLUE :

NE JAMAIS INVENTER DE FAITS.

Tu peux :

- corriger la grammaire ;
- améliorer le style ;
- restructurer les informations ;
- professionnaliser une description ;
- utiliser des verbes d'action ;
- mettre en valeur une compétence explicitement indiquée ;
- adapter le vocabulaire à une offre ;
- proposer une formulation plus claire.

Tu ne dois jamais :

- inventer une expérience ;
- inventer une entreprise ;
- inventer un diplôme ;
- inventer une certification ;
- inventer une compétence ;
- inventer une date ;
- inventer un chiffre ;
- inventer un résultat ;
- transformer une exigence de l'annonce en compétence acquise.

Si une information importante manque, utiliser :

[À compléter]

QUALITÉ :

Le résultat doit être :

- naturel ;
- professionnel ;
- précis ;
- crédible ;
- lisible ;
- adapté au poste.

ÉVITER :

- les répétitions ;
- les phrases artificielles ;
- les superlatifs excessifs ;
- les formulations vagues ;
- les emojis dans les documents professionnels ;
- les commentaires adressés à l'utilisateur dans le document.

FORMAT :

Retourner uniquement le document demandé.

Ne pas commencer par :

"Voici votre CV"

"Voici votre lettre"

"Bien sûr"

"En tant qu'IA"

Pour un CV, utiliser une structure claire avec des titres.

Pour une lettre, retourner uniquement la lettre.
"""


# ============================================================
# FONCTION UTILISÉE PAR APP.PY
# ============================================================

def build_prompts(params: dict[str, Any]) -> tuple[str, str]:
    """
    Construit le prompt système et le prompt utilisateur.

    Cette fonction est appelée directement par app.py.
    """

    if not isinstance(params, dict):
        raise TypeError(
            "Les paramètres du document doivent être un dictionnaire."
        )

    name = _clean(params.get("name"), 200)
    job = _clean(params.get("job"), 300)
    company = _clean(params.get("company"), 300)
    background = _clean(params.get("background"), 8000)
    offer = _clean(params.get("offer"), 10000)
    notes = _clean(params.get("notes"), 3000)
    doc_type = _clean(params.get("doc_type"), 100)
    language = _language_name(_clean(params.get("language")))
    tone = _clean(params.get("tone"))
    length = _clean(params.get("length"))

    system_prompt = _global_system_prompt()

    user_prompt = f"""
Tu dois maintenant créer le document demandé.

==================================================
IDENTITÉ DU CANDIDAT
==================================================

Nom et prénom :
{name}

==================================================
POSTE
==================================================

Poste visé :
{job}

Entreprise :
{company or "Non précisée"}

==================================================
PARAMÈTRES
==================================================

Type de document :
{doc_type}

Langue :
{language}

Ton :
{tone or "Professionnel"}

Longueur :
{length or "Équilibrée"}

==================================================
PARCOURS DU CANDIDAT
==================================================

{background}

==================================================
OFFRE D'EMPLOI
==================================================

{offer or "Aucune offre fournie."}

==================================================
CONSIGNES PARTICULIÈRES
==================================================

{notes or "Aucune consigne particulière."}

==================================================
INSTRUCTIONS
==================================================

1. Analyse toutes les informations.
2. Identifie les éléments utiles à la candidature.
3. Reformule les informations professionnellement.
4. Si une offre est fournie, identifie ses mots-clés pertinents.
5. Utilise uniquement les mots-clés correspondant réellement au profil.
6. Ne transforme jamais une exigence de l'annonce en compétence acquise.
7. N'invente aucune information.
8. Respecte la langue demandée.
9. Retourne directement le document final.
"""

    user_prompt += _document_instruction(params)

    return system_prompt, user_prompt


# ============================================================
# GÉNÉRATION GEMINI EN STREAMING
# ============================================================

def stream_document(
    api_key: str,
    system_prompt: str,
    user_prompt: str,
    creativity: float = 0.6,
) -> Iterator[str]:
    """
    Génère le document avec Gemini progressivement.

    Compatible avec :

        st.write_stream(
            stream_document(
                api_key,
                system_prompt,
                user_prompt,
                creativity,
            )
        )
    """

    api_key = _clean(api_key)

    if not api_key:
        raise ValueError(
            "La clé API Gemini est absente. "
            "Ajoutez GEMINI_API_KEY dans les secrets."
        )

    try:
        temperature = float(creativity)
    except (TypeError, ValueError):
        temperature = 0.6

    temperature = max(0.0, min(1.0, temperature))

    try:
        client = genai.Client(api_key=api_key)

        response_stream = client.models.generate_content_stream(
            model=DEFAULT_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
                max_output_tokens=8192,
            ),
        )

        received_text = False

        for chunk in response_stream:
            text = getattr(chunk, "text", None)

            if text:
                received_text = True
                yield text

        if not received_text:
            raise RuntimeError(
                "Gemini n'a retourné aucun contenu exploitable."
            )

    except Exception as exc:
        message = str(exc).strip()

        if not message:
            message = "Erreur inconnue lors de la communication avec Gemini."

        raise RuntimeError(
            f"Erreur Gemini : {message}"
        ) from exc


# ============================================================
# APPEL GEMINI STANDARD
# ============================================================

def _generate_text(
    api_key: str,
    system_instruction: str,
    prompt: str,
    creativity: float = 0.4,
) -> str:
    """Effectue un appel Gemini non-streaming."""

    api_key = _clean(api_key)

    if not api_key:
        raise ValueError("La clé API Gemini est absente.")

    try:
        temperature = float(creativity)
    except (TypeError, ValueError):
        temperature = 0.4

    temperature = max(0.0, min(1.0, temperature))

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            max_output_tokens=8192,
        ),
    )

    result = getattr(response, "text", None)

    if not result:
        raise RuntimeError(
            "Gemini n'a retourné aucun texte."
        )

    return result.strip()


# ============================================================
# ANALYSE CV
# ============================================================

def analyze_cv(
    api_key: str,
    cv_text: str,
    job_offer: str = "",
) -> str:
    """Analyse un CV."""

    cv_text = _clean(cv_text, 20000)
    job_offer = _clean(job_offer, 12000)

    if not cv_text:
        raise ValueError("Le CV est vide.")

    prompt = f"""
Analyse professionnellement le CV suivant.

CV :
{cv_text}

OFFRE CIBLE :
{job_offer or "Aucune offre fournie."}

Retourne :

1. LISIBILITÉ
2. POINTS FORTS
3. POINTS À AMÉLIORER
4. COMPÉTENCES IDENTIFIÉES
5. MOTS-CLÉS PERTINENTS
6. PROFIL PROFESSIONNEL
7. EXPÉRIENCES
8. STRUCTURE
9. RECOMMANDATIONS CONCRÈTES

Si une offre est fournie, indique les éléments demandés qui ne sont pas
identifiables dans le CV.

Les éventuels scores sont indicatifs et ne garantissent pas un recrutement.
Ne déduis pas une compétence qui n'est pas présente dans le CV.
"""

    return _generate_text(
        api_key,
        _global_system_prompt(),
        prompt,
        creativity=0.25,
    )


# ============================================================
# ANALYSE OFFRE
# ============================================================

def analyze_job_offer(
    api_key: str,
    job_offer: str,
) -> str:
    """Analyse une offre d'emploi."""

    job_offer = _clean(job_offer, 15000)

    if not job_offer:
        raise ValueError("L'offre d'emploi est vide.")

    prompt = f"""
Analyse l'offre d'emploi suivante.

OFFRE :
{job_offer}

Identifie :

- intitulé du poste ;
- missions principales ;
- compétences techniques ;
- qualités professionnelles ;
- outils ou logiciels ;
- diplômes demandés ;
- certifications demandées ;
- expérience demandée ;
- langues demandées ;
- mots-clés importants ;
- éléments indispensables ;
- éléments souhaités.

Ne transforme pas une préférence en obligation.
"""

    return _generate_text(
        api_key,
        _global_system_prompt(),
        prompt,
        creativity=0.2,
    )


# ============================================================
# CORRESPONDANCE CV / OFFRE
# ============================================================

def match_cv_to_offer(
    api_key: str,
    cv_text: str,
    job_offer: str,
) -> str:
    """Compare un CV à une offre."""

    cv_text = _clean(cv_text, 20000)
    job_offer = _clean(job_offer, 15000)

    if not cv_text:
        raise ValueError("Le CV est vide.")

    if not job_offer:
        raise ValueError("L'offre d'emploi est vide.")

    prompt = f"""
Compare objectivement le CV et l'offre suivants.

CV :
{cv_text}

OFFRE :
{job_offer}

Retourne :

CORRESPONDANCE GLOBALE

COMPÉTENCES CORRESPONDANTES

COMPÉTENCES DEMANDÉES NON IDENTIFIÉES

MOTS-CLÉS À ENVISAGER

POINTS À REFORMULER

RECOMMANDATIONS

Pour chaque compétence identifiée, base-toi uniquement sur les informations
présentes dans le CV.

Ne conseille jamais au candidat de prétendre posséder une compétence qu'il
ne possède pas.

Toute correspondance est indicative et ne garantit pas une sélection.
"""

    return _generate_text(
        api_key,
        _global_system_prompt(),
        prompt,
        creativity=0.25,
    )


# ============================================================
# AMÉLIORATION CV
# ============================================================

def improve_cv(
    api_key: str,
    cv_text: str,
    job_offer: str = "",
    language: str = "Français",
) -> str:
    """Améliore un CV sans inventer d'informations."""

    cv_text = _clean(cv_text, 25000)
    job_offer = _clean(job_offer, 15000)
    language = _language_name(language)

    if not cv_text:
        raise ValueError("Le CV à améliorer est vide.")

    prompt = f"""
Améliore professionnellement le CV suivant.

LANGUE :
{language}

CV ORIGINAL :
{cv_text}

OFFRE CIBLE :
{job_offer or "Aucune offre fournie."}

OBJECTIFS :

- améliorer la structure ;
- améliorer la lisibilité ;
- renforcer le profil professionnel ;
- améliorer les descriptions d'expérience ;
- utiliser des verbes d'action ;
- améliorer la présentation des compétences ;
- supprimer les répétitions ;
- adapter le vocabulaire à l'offre si elle est fournie.

RÈGLE ABSOLUE :

Ne crée aucune information.

Conserve les faits, dates, entreprises et expériences fournis.

Si une information importante manque :
[À compléter]

Retourne uniquement le CV amélioré.
"""

    return _generate_text(
        api_key,
        _global_system_prompt(),
        prompt,
        creativity=0.35,
    )


# ============================================================
# PROFIL PROFESSIONNEL
# ============================================================

def generate_profile(
    api_key: str,
    background: str,
    target_job: str = "",
    language: str = "Français",
) -> str:
    """Génère un profil professionnel."""

    background = _clean(background, 10000)
    target_job = _clean(target_job, 500)
    language = _language_name(language)

    if not background:
        raise ValueError("Le parcours du candidat est vide.")

    prompt = f"""
Crée un profil professionnel de 4 à 7 lignes.

LANGUE :
{language}

POSTE CIBLE :
{target_job or "Non précisé"}

PARCOURS :
{background}

Le profil doit :

- être crédible ;
- être précis ;
- présenter les compétences réellement indiquées ;
- mettre en valeur les qualités professionnelles présentes ;
- être adapté au poste cible si celui-ci est fourni.

Ne pas inventer d'expérience, diplôme, chiffre ou compétence.

Retourne uniquement le profil.
"""

    return _generate_text(
        api_key,
        _global_system_prompt(),
        prompt,
        creativity=0.35,
    )


# ============================================================
# REFORMULATION D'EXPÉRIENCE
# ============================================================

def rewrite_experience(
    api_key: str,
    experience: str,
    language: str = "Français",
) -> str:
    """Transforme une description simple en formulation professionnelle."""

    experience = _clean(experience, 6000)
    language = _language_name(language)

    if not experience:
        raise ValueError("La description de l'expérience est vide.")

    prompt = f"""
Reformule professionnellement cette expérience.

LANGUE :
{language}

DESCRIPTION :
{experience}

Propose plusieurs formulations possibles.

Elles doivent être directement utilisables dans un CV.

N'invente aucun fait.
"""

    return _generate_text(
        api_key,
        _global_system_prompt(),
        prompt,
        creativity=0.4,
    )


# ============================================================
# TRADUCTION
# ============================================================

def translate_document(
    api_key: str,
    document: str,
    target_language: str,
) -> str:
    """Traduit un document professionnel."""

    document = _clean(document, 30000)
    target_language = _language_name(target_language)

    if not document:
        raise ValueError("Le document à traduire est vide.")

    prompt = f"""
Traduis et adapte professionnellement le document suivant en
{target_language}.

DOCUMENT :

{document}

Consignes :

- conserver les informations factuelles ;
- conserver la structure ;
- employer un vocabulaire professionnel naturel ;
- éviter une traduction mot à mot lorsqu'une formulation naturelle est
  préférable ;
- ne rien inventer ;
- ne rien supprimer d'important.

Retourne uniquement le document traduit.
"""

    return _generate_text(
        api_key,
        _global_system_prompt(),
        prompt,
        creativity=0.2,
    )


# ============================================================
# CV EXPRESS
# ============================================================

def cv_express(
    api_key: str,
    description: str,
    language: str = "Français",
    target_job: str = "",
) -> str:
    """Crée un CV rapidement à partir d'une description libre."""

    description = _clean(description, 12000)
    language = _language_name(language)
    target_job = _clean(target_job, 500)

    if not description:
        raise ValueError("La description du candidat est vide.")

    prompt = f"""
Crée un CV professionnel à partir de la description suivante.

LANGUE :
{language}

POSTE RECHERCHÉ :
{target_job or "À déterminer à pa
