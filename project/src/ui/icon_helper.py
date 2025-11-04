from typing import Optional


def display_icon_text(raw: Optional[str]) -> str:
    """Mapea nombres de íconos a emojis visibles.

    Soporta: "atom", "link", "flask", "beaker".
    Si no hay mapeo, retorna el valor original o un emoji por defecto.
    """
    if not raw:
        return "📘"
    key = raw.strip().lower()
    mapping = {
        "atom": "⚛️",
        "link": "🔗",
        "flask": "🧪",
        "beaker": "⚗️",
    }
    return mapping.get(key, raw)