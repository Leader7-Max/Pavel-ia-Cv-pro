"""Génération du CV / de la lettre avec Gemini."""

try:
    from google import genai
    from google.genai import types
except ImportError:  # paquet absent : l'appli s'ouvre quand même et explique le problème
    genai = types = None

from config import LENGTHS, MODELS


# ─────────────────────────────────────────────────────────────
# Génération IA
# ─────────────────────────────────────────────────────────────
def build_prompts(p: dict) -> tuple[str, str]:
    is_cv = p["doc_type"].startswith("CV")
    kind = "cv" if is_cv else "lettre"
    length = LENGTHS[kind][p["length"]]

    if is_cv:
        structure = (
            "STRUCTURE DU CV (chaque titre de section en MAJUSCULES, seul sur sa ligne) :\n"
            "- Ligne 1 : nom et prénom. Ligne 2 : intitulé du poste visé.\n"
            "- Ligne 3 : coordonnées sur une seule ligne, séparées par « | » "
            "(seulement celles fournies : e-mail, téléphone, ville, lien).\n"
            "- PROFIL : 3 lignes maximum.\n"
            "- COMPÉTENCES CLÉS : liste courte, orientée vers l'offre.\n"
            "- EXPÉRIENCES PROFESSIONNELLES : pour chaque expérience, une ligne "
            "« Poste, Structure (période) » puis des puces commençant par un verbe d'action "
            "et, si possible, un résultat.\n"
            "- FORMATION\n"
            "- LANGUES ET ATOUTS (si pertinent)\n"
            f"Le CV {length}."
        )
    else:
        structure = (
            "STRUCTURE DE LA LETTRE :\n"
            "- Coordonnées du candidat (celles fournies ; entre crochets si inconnues), "
            "lieu et date, destinataire.\n"
            "- Objet.\n"
            "- Formule d'appel.\n"
            "- 3 ou 4 paragraphes : accroche personnalisée, valeur ajoutée du candidat "
            "avec des exemples concrets, motivation pour l'entreprise, ouverture vers un entretien.\n"
            "- Formule de politesse et signature.\n"
            f"La lettre fait {length}."
        )

    system = (
        "Tu es un expert en recrutement et en rédaction de CV et de lettres de motivation, "
        "capable d'écrire des documents optimisés pour les logiciels de tri (ATS) tout en "
        "restant agréables à lire pour un recruteur. Le candidat n'est pas forcément à l'aise "
        "avec le français : améliore ses phrases et corrige ses fautes sans changer le sens.\n"
        "RÈGLES ABSOLUES :\n"
        "1. N'invente JAMAIS de fait : employeur, diplôme, date, chiffre ou outil absent des "
        "informations fournies. Si une information utile manque, insère un champ entre "
        "crochets, par exemple [ville] ou [chiffre à préciser].\n"
        "2. Écris en texte brut : pas de Markdown, pas de titres avec #, pas de gras. "
        "Utilise « • » pour les puces.\n"
        "3. Style clair, concret, sans formules creuses ni superlatifs inutiles.\n"
        f"4. Rédige en {p['language']}.\n"
        "5. Réponds uniquement avec le document final, sans commentaire avant ni après.\n"
        "6. Si le candidat donne une demande spéciale, suis-la en priorité pour le style et "
        "l'accent du document, mais sans jamais violer la règle 1."
    )

    def line(label: str, value) -> str:
        return f"- {label} : {value}\n" if value else ""

    quick = "; ".join(p.get("quick") or [])
    special = p.get("special") or ""
    request = "\n".join(x for x in (quick, special) if x) or "Aucune"

    offer = p.get("offer") or "Aucune offre fournie. Base-toi sur les standards du poste visé."
    prompt = (
        f"Rédige : {p['doc_type']}\n\n"
        "INFORMATIONS SUR LE CANDIDAT\n"
        + line("Nom et prénom", p["name"])
        + line("E-mail", p.get("email"))
        + line("Téléphone", p.get("phone"))
        + line("Ville et pays", p.get("city"))
        + line("Lien (LinkedIn ou site)", p.get("link"))
        + line("Poste visé", p["job"])
        + line("Entreprise ciblée", p.get("company") or "Non précisée")
        + line("Expériences de travail", p["background"])
        + line("Études et diplômes", p.get("education"))
        + line("Compétences", p.get("skills"))
        + line("Langues parlées", p.get("languages_spoken"))
        + line("Qualités", p.get("strengths"))
        + line("Ton souhaité", p["tone"])
        + f"\nDEMANDE SPÉCIALE DU CANDIDAT\n{request}\n"
        f"\nOFFRE D'EMPLOI DE RÉFÉRENCE\n{offer}\n\n{structure}\n\n"
        "Si une offre est fournie, reprends naturellement ses mots-clés et compétences "
        "attendues, uniquement lorsqu'ils correspondent au parcours du candidat."
    )
    return system, prompt


def stream_document(api_key: str, system: str, prompt: str, temperature: float):
    """Génère le texte en flux continu, avec un modèle de secours si le premier échoue."""
    if genai is None:
        raise RuntimeError(
            "Le paquet google-genai n'est pas installé. Ajoutez la ligne « google-genai » "
            "dans requirements.txt (sans google-generativeai), puis redémarrez l'application."
        )
    client = genai.Client(api_key=api_key)
    last_error = None
    for model in MODELS:
        started = False
        try:
            stream = client.models.generate_content_stream(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system,
                    temperature=temperature,
                ),
            )
            for chunk in stream:
                if chunk.text:
                    started = True
                    yield chunk.text
            if started:
                return
            last_error = RuntimeError("Réponse vide du modèle.")
        except Exception as err:  # noqa: BLE001
            if started:
                raise  # flux interrompu en cours de route : inutile de relancer
            last_error = err
    raise last_error


# Filet de sécurité : si Streamlit lance ce fichier par erreur comme fichier principal
# (page blanche), on démarre quand même l'interface définie dans app.py.
if __name__ == "__main__":
    import runpy
    from pathlib import Path

    runpy.run_path(str(Path(__file__).with_name("app.py")), run_name="__main__")
    
