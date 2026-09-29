"""Pavel IA CV - moteur IA Gemini pour CV, lettres et candidatures."""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import Any

from google import genai
from google.genai import types


DEFAULT_MODEL = "gemini-2.5-flash"


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


def _clean(value: Any, maximum: int | None = None) -> str:
    if value is None:
        return ""

    text = str(value).strip()

    if maximum is not None:
        text = text[:maximum]

    return text


def _language_name(language: str) -> str:
    return SUPPORTED_LANGUAGES.get(language, language or "français")


def _document_instruction(params: dict[str, Any]) -> str:
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

        return (
            "Produis un CV en "
            f"{language}. "
            f"Poste cible : {job or 'à déterminer'}. "
            f"Entreprise cible : {company or 'non précisée'}. "
            f"Longueur souhaitée : {length or 'équilibrée'}. "
            f"Style : {format_hint}. "
            f"Ton : {tone or 'professionnel'}. "
            "Structure le CV avec des rubriques clairement identifiables. "
            "Mets en avant les résultats, compétences et réalisations. "
            "N'invente aucune expérience, date, diplôme, entreprise, "
            "certification, compétence ou information personnelle. "
            "Lorsque l'information manque, utilise une formulation prudente "
            "ou laisse la donnée à compléter."
        )

    return (
        "Produis une lettre de motivation en "
        f"{language}. "
        f"Poste ciblé : {job or 'à déterminer'}. "
        f"Entreprise : {company or 'non précisée'}. "
        f"Longueur : {length or 'équilibrée'}. "
        f"Ton : {tone or 'professionnel'}. "
        "La lettre doit être personnalisée à partir des informations "
        "fournies et de l'offre d'emploi. "
        "Évite les phrases génériques et les affirmations non vérifiées. "
        "N'invente aucune expérience ou qualification."
    )


def _global_system_prompt() -> str:
    return (
        "Tu es Pavel IA CV, un assistant spécialisé dans les candidatures "
        "professionnelles. Tu aides à créer, améliorer, analyser et adapter "
        "des CV et lettres de motivation. "
        "Tu dois être précis, professionnel, naturel et orienté recrutement. "
        "Respecte strictement les informations fournies par l'utilisateur. "
        "N'invente jamais de faits personnels ou professionnels. "
        "Tu peux reformuler une information existante pour la rendre plus "
        "claire et convaincante, sans changer son sens. "
        "Évite les emojis dans les documents professionnels sauf demande "
        "expresse. "
        "Réponds directement avec le contenu demandé, sans préambule "
        "inutile."
    )


def build_prompts(params: dict[str, Any]) -> tuple[str, str]:
    system_prompt = _global_system_prompt()

    document_instruction = _document_instruction(params)

    name = _clean(params.get("name"))
    job = _clean(params.get("job"))
    company = _clean(params.get("company"))
    language = _language_name(_clean(params.get("language")))
    background = _clean(params.get("background"), 12000)
    job_offer = _clean(params.get("job_offer"), 15000)
    notes = _clean(params.get("notes"), 8000)
    doc_type = _clean(params.get("doc_type"))

    user_prompt = (
        f"TYPE DE DOCUMENT : {doc_type or 'candidature'}\n"
        f"LANGUE : {language}\n"
        f"NOM : {name or 'non renseigné'}\n"
        f"POSTE CIBLE : {job or 'non renseigné'}\n"
        f"ENTREPRISE : {company or 'non renseignée'}\n\n"
        f"INSTRUCTIONS DE FORMAT :\n{document_instruction}\n\n"
        "PROFIL / PARCOURS FOURNI PAR L'UTILISATEUR :\n"
        f"{background or 'Aucune information supplémentaire fournie.'}\n\n"
        "OFFRE D'EMPLOI :\n"
        f"{job_offer or 'Aucune offre fournie.'}\n\n"
        "NOTES OU CONSIGNES SUPPLÉMENTAIRES :\n"
        f"{notes or 'Aucune.'}\n\n"
        "Consigne finale : crée un document directement utilisable pour une "
        "candidature. Ne crée pas de faits qui ne figurent pas dans les "
        "informations fournies."
    )

    return system_prompt, user_prompt


def _temperature(creativity: float) -> float:
    try:
        value = float(creativity)
    except (TypeError, ValueError):
        value = 0.6

    return max(0.0, min(1.0, value))


def _client(api_key: str) -> genai.Client:
    key = _clean(api_key)

    if not key:
        raise ValueError("Clé API Gemini manquante.")

    return genai.Client(api_key=key)


def stream_document(
    api_key: str,
    system_prompt: str,
    user_prompt: str,
    creativity: float = 0.6,
) -> Iterator[str]:
    client = _client(api_key)

    response_stream = client.models.generate_content_stream(
        model=DEFAULT_MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=_temperature(creativity),
            max_output_tokens=8192,
        ),
    )

    for chunk in response_stream:
        text = getattr(chunk, "text", None)

        if text:
            yield text


def _generate_text(
    api_key: str,
    system_prompt: str,
    user_prompt: str,
    creativity: float = 0.4,
    max_output_tokens: int = 8192,
) -> str:
    client = _client(api_key)

    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=_temperature(creativity),
            max_output_tokens=max_output_tokens,
        ),
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError("Gemini n'a renvoyé aucun contenu.")

    return text.strip()


def analyze_cv(api_key: str, cv_text: str) -> str:
    system = _global_system_prompt() + (
        " Analyse les CV comme un recruteur et un spécialiste ATS. "
        "Sépare clairement les points forts, les éléments à améliorer, "
        "les mots-clés, la lisibilité et les informations manquantes."
    )

    prompt = (
        "Analyse le CV ci-dessous.\n\n"
        "CV :\n"
        f"{_clean(cv_text, 30000)}\n\n"
        "Retourne une analyse structurée avec :\n"
        "1. Points forts\n"
        "2. Points à améliorer\n"
        "3. Compatibilité ATS\n"
        "4. Mots-clés utiles\n"
        "5. Informations manquantes\n"
        "6. Actions concrètes à effectuer"
    )

    return _generate_text(api_key, system, prompt)


def analyze_job_offer(api_key: str, job_offer: str) -> str:
    system = _global_system_prompt() + (
        " Analyse les offres d'emploi afin d'identifier les attentes "
        "explicites et implicites sans inventer d'informations."
    )

    prompt = (
        "Analyse cette offre d'emploi.\n\n"
        f"{_clean(job_offer, 30000)}\n\n"
        "Retourne :\n"
        "1. Poste et missions\n"
        "2. Compétences demandées\n"
        "3. Expérience demandée\n"
        "4. Mots-clés ATS\n"
        "5. Qualités recherchées\n"
        "6. Éléments importants à mettre dans le CV\n"
        "7. Points à vérifier avant candidature"
    )

    return _generate_text(api_key, system, prompt)


def match_cv_to_offer(
    api_key: str,
    cv_text: str,
    job_offer: str,
) -> str:
    system = _global_system_prompt() + (
        " Compare objectivement un CV avec une offre. "
        "Ne fabrique pas de pourcentage de compatibilité sans calcul "
        "explicite et ne présente pas une estimation comme un fait."
    )

    prompt = (
        "Compare les deux contenus suivants.\n\n"
        "CV :\n"
        f"{_clean(cv_text, 30000)}\n\n"
        "OFFRE :\n"
        f"{_clean(job_offer, 30000)}\n\n"
        "Présente :\n"
        "1. Correspondances\n"
        "2. Compétences présentes mais peu visibles\n"
        "3. Compétences demandées absentes du CV\n"
        "4. Mots-clés à intégrer uniquement s'ils sont réellement justifiés\n"
        "5. Modifications recommandées\n"
        "6. Risques ou incohérences éventuels"
    )

    return _generate_text(api_key, system, prompt)


def improve_cv(
    api_key: str,
    cv_text: str,
    target_job: str = "",
) -> str:
    system = _global_system_prompt()

    target = _clean(target_job) or "poste correspondant au profil"

    prompt = (
        f"Améliore ce CV pour le poste suivant : {target}.\n\n"
        f"CV actuel :\n{_clean(cv_text, 30000)}\n\n"
        "Conserve toutes les informations vérifiables. "
        "Améliore la formulation, la structure, la précision et les mots-clés "
        "pertinents. Ne crée aucune expérience, date ou qualification."
    )

    return _generate_text(api_key, system, prompt)


def generate_profile(
    api_key: str,
    cv_text: str,
    language: str = "Français",
) -> str:
    lang = _language_name(language)

    system = _global_system_prompt()

    prompt = (
        f"À partir du CV suivant, rédige un profil professionnel en {lang}.\n\n"
        f"{_clean(cv_text, 20000)}\n\n"
        "Fournis un résumé professionnel court, naturel et crédible, "
        "adapté au haut d'un CV ou à un profil professionnel en ligne. "
        "N'ajoute aucune information absente du CV."
    )

    return _generate_text(api_key, system, prompt)


def rewrite_experience(
    api_key: str,
    experience: str,
    target_job: str = "",
) -> str:
    target = _clean(target_job) or "poste ciblé"

    system = _global_system_prompt()

    prompt = (
        f"Réécris cette expérience pour une candidature au poste de {target}.\n\n"
        f"Expérience originale :\n{_clean(experience, 12000)}\n\n"
        "Utilise des verbes d'action et une formulation professionnelle. "
        "Valorise les responsabilités et résultats lorsqu'ils sont présents. "
        "Ne transforme pas une responsabilité en résultat chiffré inventé."
    )

    return _generate_text(api_key, system, prompt)


def translate_document(
    api_key: str,
    document: str,
    target_language: str,
) -> str:
    language = _language_name(target_language)

    system = _global_system_prompt()

    prompt = (
        f"Traduis le document professionnel suivant en {language}.\n\n"
        f"{_clean(document, 30000)}\n\n"
        "Conserve le sens, les noms propres, les dates et les informations "
        "factuelles. Adapte les formulations au contexte professionnel de "
        "la langue cible sans inventer de contenu."
    )

    return _generate_text(
        api_key,
        system,
        prompt,
        creativity=0.2,
    )


def cv_express(
    api_key: str,
    name: str,
    target_job: str,
    background: str,
    language: str = "Français",
) -> str:
    lang = _language_name(language)

    system = _global_system_prompt()

    prompt = (
        f"Crée un CV Express en {lang}.\n\n"
        f"Nom : {_clean(name)}\n"
        f"Poste ciblé : {_clean(target_job)}\n"
        f"Parcours et compétences : {_clean(background, 20000)}\n\n"
        "Structure : titre professionnel, profil, compétences, expériences "
        "ou projets, formation et informations complémentaires lorsque "
        "disponibles. Si une rubrique n'est pas documentée, ne l'invente pas."
    )

    return _generate_text(api_key, system, prompt)


def sanitize_document(document: str) -> str:
    text = _clean(document)

    replacements = {
        "\r\n": "\n",
        "\r": "\n",
        "\u00a0": " ",
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\n{4,}", "\n\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text.strip()


__all__ = [
    "DEFAULT_MODEL",
    "SUPPORTED_LANGUAGES",
    "CV_FORMATS",
    "build_prompts",
    "stream_document",
    "analyze_cv",
    "analyze_job_offer",
    "match_cv_to_offer",
    "improve_cv",
    "generate_profile",
    "rewrite_experience",
    "translate_document",
    "cv_express",
    "sanitize_document",
    ]    ),
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
