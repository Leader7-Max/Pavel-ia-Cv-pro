"""Fonctions utilitaires : statistiques, secrets, nettoyage de texte, mots-clés."""

import json
import re
import threading
from collections import Counter
from pathlib import Path

import streamlit as st

# ─────────────────────────────────────────────────────────────
# Statistiques réelles (persistées dans un fichier JSON)
# ─────────────────────────────────────────────────────────────
STATS_FILE = Path("stats.json")
_STATS_LOCK = threading.Lock()
DEFAULT_STATS = {"likes": 0, "generations": 0}


def load_stats() -> dict:
    try:
        data = json.loads(STATS_FILE.read_text(encoding="utf-8"))
        return {k: int(data.get(k, v)) for k, v in DEFAULT_STATS.items()}
    except Exception:  # noqa: BLE001
        return dict(DEFAULT_STATS)


def bump_stat(key: str) -> dict:
    """Incrémente un compteur de façon sûre (verrou + écriture tolérante aux erreurs)."""
    with _STATS_LOCK:
        stats = load_stats()
        stats[key] = stats.get(key, 0) + 1
        try:
            STATS_FILE.write_text(json.dumps(stats), encoding="utf-8")
        except OSError:
            pass  # système de fichiers en lecture seule : on ignore
        return stats


# ─────────────────────────────────────────────────────────────
# Utilitaires
# ─────────────────────────────────────────────────────────────
def get_secret(name: str, default: str = "") -> str:
    """Lit une valeur dans les secrets Streamlit sans planter si absents."""
    try:
        return str(st.secrets.get(name, default) or default)
    except Exception:  # noqa: BLE001
        return default


def slugify(value: str) -> str:
    return re.sub(r"[^\w-]+", "_", value.strip(), flags=re.UNICODE).strip("_") or "document"


def clean_output(text: str) -> str:
    """Retire le Markdown résiduel pour obtenir un texte brut réutilisable."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"^\s*[\*\-•]\s+", "• ", text, flags=re.M)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def friendly_error(err: Exception) -> str:
    msg = str(err).lower()
    # Expressions précises : « rate » seul apparaît dans « generate », d'où de faux positifs.
    if re.search(r"api key|api_key|permission|unauthenticated|\b40[13]\b", msg):
        return "La clé API est refusée. Vérifiez qu'elle est correcte et active."
    if re.search(r"\b429\b|quota|rate limit|resource_exhausted", msg):
        return "La limite d'utilisation de l'API est atteinte. Réessayez dans une minute."
    if re.search(r"\b503\b|overloaded|unavailable", msg):
        return "Le service de rédaction est saturé. Réessayez dans quelques instants."
    return f"La génération a échoué. Détail technique : {err}"


STOPWORDS = set(
    """
    dans pour avec vous nous votre notre vos nos être sera seront cette cettes entre leurs leur
    aussi ainsi alors plus moins comme chez sous sont elle elles ils dont mais donc car
    poste offre mission missions profil candidat entreprise société travail équipe
    recherchons rejoindre rejoignez avoir faire tous toutes tout toute très bien
    """.split()
)


def extract_keywords(text: str, top: int = 20) -> list[str]:
    words = re.findall(r"[a-zà-ÿœ][a-zà-ÿœ'-]{4,}", text.lower())
    counts = Counter(w for w in words if w not in STOPWORDS)
    return [w for w, _ in counts.most_common(top)]


def keyword_match(offer: str, document: str):
    keywords = extract_keywords(offer)
    if not keywords:
        return None
    doc = document.lower()
    missing = [k for k in keywords if k not in doc]
    return len(keywords) - len(missing), len(keywords), missing
