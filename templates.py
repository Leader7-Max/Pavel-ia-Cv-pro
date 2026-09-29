"""Modèles de mise en page (CV et lettres) : couleurs, polices, style de l'en-tête."""

DEFAULT_TEMPLATE = "Classique"

# Couleurs en RVB. band = couleur du bandeau d'en-tête (None = pas de bandeau).
TEMPLATES = {
    "Classique": {
        "desc": "Sobre et lisible, accents turquoise et ambre.",
        "font_pdf": "Helvetica", "font_docx": "Calibri", "serif": False,
        "pdf_size": 10.5, "docx_size": 10.5, "name_size": 22, "head_size": 11,
        "body": (38, 52, 56), "name": (18, 39, 43), "sub": (14, 107, 107),
        "head": (14, 107, 107), "rule": (220, 227, 229), "accent": (242, 169, 59),
        "band": None, "center": False, "head_style": "line",
    },
    "Moderne": {
        "desc": "Bandeau d'en-tête bleu nuit, filets corail.",
        "font_pdf": "Helvetica", "font_docx": "Calibri", "serif": False,
        "pdf_size": 10.5, "docx_size": 10.5, "name_size": 24, "head_size": 11,
        "body": (40, 44, 52), "name": (255, 255, 255), "sub": (200, 214, 235),
        "head": (31, 58, 95), "rule": (224, 122, 95), "accent": (224, 122, 95),
        "band": (31, 58, 95), "center": False, "head_style": "line",
    },
    "Élégant": {
        "desc": "Police à empattements, en-tête centré, filets dorés.",
        "font_pdf": "Times", "font_docx": "Georgia", "serif": True,
        "pdf_size": 11.5, "docx_size": 10.5, "name_size": 24, "head_size": 11.5,
        "body": (45, 45, 45), "name": (34, 34, 34), "sub": (120, 98, 62),
        "head": (34, 34, 34), "rule": (176, 141, 87), "accent": (176, 141, 87),
        "band": None, "center": True, "head_style": "line",
    },
    "Minimaliste": {
        "desc": "Noir et blanc, épuré et compact.",
        "font_pdf": "Helvetica", "font_docx": "Arial", "serif": False,
        "pdf_size": 10, "docx_size": 10, "name_size": 20, "head_size": 10.5,
        "body": (30, 30, 30), "name": (0, 0, 0), "sub": (90, 90, 90),
        "head": (0, 0, 0), "rule": (160, 160, 160), "accent": None,
        "band": None, "center": False, "head_style": "plain",
    },
}


def get_template(name: str) -> dict:
    return TEMPLATES.get(name, TEMPLATES[DEFAULT_TEMPLATE])


def _rgb(color) -> str:
    return "rgb(%d,%d,%d)" % tuple(color)


def preview_html(name: str) -> str:
    """Petite vignette HTML qui donne une idée du modèle choisi."""
    t = get_template(name)
    family = "Georgia, 'Times New Roman', serif" if t["serif"] else "'DM Sans', Arial, sans-serif"
    align = "center" if t["center"] else "left"
    accent_margin = "8px auto 0" if t["center"] else "8px 0 0"

    if t["band"]:
        header = (
            f'<div style="background:{_rgb(t["band"])};padding:14px 16px;text-align:{align}">'
            f'<div style="font-weight:700;font-size:1.15rem;color:#fff">Prénom Nom</div>'
            f'<div style="font-size:.85rem;color:{_rgb(t["sub"])}">Poste visé</div></div>'
        )
    else:
        underline = (
            f'<div style="width:40px;height:3px;background:{_rgb(t["accent"])};margin:{accent_margin}"></div>'
            if t["accent"] else ""
        )
        header = (
            f'<div style="padding:14px 16px 0;text-align:{align}">'
            f'<div style="font-weight:700;font-size:1.15rem;color:{_rgb(t["name"])}">Prénom Nom</div>'
            f'<div style="font-size:.85rem;color:{_rgb(t["sub"])}">Poste visé</div>{underline}</div>'
        )

    border = f"border-bottom:1px solid {_rgb(t['rule'])};" if t["head_style"] == "line" else ""
    bar = "height:6px;border-radius:3px;background:#E4E9EB;margin:6px 0;"

    def section(title: str) -> str:
        return (
            f'<div style="font-weight:700;font-size:.72rem;letter-spacing:.04em;'
            f'color:{_rgb(t["head"])};{border}padding-bottom:3px;margin-top:12px">{title}</div>'
            f'<div style="{bar}width:92%"></div><div style="{bar}width:76%"></div>'
        )

    return (
        f'<div style="font-family:{family};background:#fff;border:1px solid #DCE3E5;'
        f'border-radius:10px;overflow:hidden;max-width:340px;margin:.3rem 0 1rem">'
        f'{header}<div style="padding:0 16px 14px">{section("PROFIL")}{section("EXPÉRIENCES")}</div></div>'
      )
  
