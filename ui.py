"""Éléments visuels sur mesure (HTML) : bandeau d'accueil, étapes, titres de section."""

# Logo version « verre dépoli » pour le fond dégradé du bandeau.
LOGO_MARK = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Logo Pavel IA CV">'
    '<rect x="1" y="1" width="62" height="62" rx="16" fill="rgba(255,255,255,.16)" '
    'stroke="rgba(255,255,255,.45)" stroke-width="2"/>'
    '<path d="M18 12h18l10 10v26a3 3 0 0 1-3 3H18a3 3 0 0 1-3-3V15a3 3 0 0 1 3-3z" fill="#FFFFFF"/>'
    '<path d="M36 12v7a3 3 0 0 0 3 3h7z" fill="#B7D6D6"/>'
    '<rect x="21" y="27" width="16" height="3" rx="1.5" fill="#0E6B6B"/>'
    '<rect x="21" y="34" width="11" height="3" rx="1.5" fill="#9CC3C3"/>'
    '<circle cx="44" cy="44" r="10" fill="#F2A93B" stroke="#FFFFFF" stroke-width="3"/>'
    '<path d="M39.5 44.5l3.3 3.3 6-6.6" fill="none" stroke="#12272B" stroke-width="2.8" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

STEPS = ["Informations", "Rédaction", "Téléchargement"]


def hero_html() -> str:
    """Bandeau d'accueil : dégradé animé, promesse, points forts et CV miniature."""
    return (
        '<div class="hero">'
        '<div class="hero-doc" aria-hidden="true"><i class="n"></i><i class="a"></i>'
        '<i></i><i></i><i style="width:70%"></i><b>✓</b></div>'
        f'<div class="hero-head">{LOGO_MARK}<h1>Pavel IA CV</h1></div>'
        "<p class=\"hero-sub\">Un CV ou une lettre de motivation adaptés à l'offre, "
        "prêts à télécharger.</p>"
        '<div class="pills"><span>✓ Adapté à l\'offre</span><span>✓ Compatible ATS</span>'
        "<span>✓ PDF et Word</span></div>"
        "</div>"
    )


def stepper_html(current: int) -> str:
    """Barre de progression en 3 étapes (1 = informations, 2 = rédaction, 3 = téléchargement)."""
    parts = []
    for index, label in enumerate(STEPS, start=1):
        state = "done" if index < current else "active" if index == current else "todo"
        dot = "✓" if state == "done" else str(index)
        parts.append(
            f'<div class="step {state}"><span class="dot">{dot}</span><span class="lbl">{label}</span></div>'
        )
        if index < len(STEPS):
            parts.append(f'<div class="bar{" done" if index < current else ""}"></div>')
    return f'<div class="stepper">{"".join(parts)}</div>'


def section_html(icon: str, title: str) -> str:
    """Titre de section avec pastille colorée."""
    return f'<div class="sect"><span class="ico">{icon}</span><span>{title}</span></div>'


def ready_html(kind: str) -> str:
    """Bandeau de confirmation affiché quand le document est prêt."""
    return (
        '<div class="ready"><span class="tick">✓</span><div>'
        f"<strong>Votre {kind} est prêt</strong>"
        "<span>Relisez-le, modifiez-le si besoin, puis choisissez un modèle et téléchargez-le.</span>"
        "</div></div>"
    )
  
