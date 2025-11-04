from pathlib import Path
from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt


def _icons_dir() -> Path:
    # project/src/ui/assets.py -> parents[2] == project
    base = Path(__file__).resolve().parents[2]
    icons = base / "assets" / "icons"
    icons.mkdir(parents=True, exist_ok=True)
    return icons


def _generate_emoji_icon(emoji: str, name: str, size: int = 64) -> Path:
    path = _icons_dir() / f"{name}.png"
    if path.exists():
        return path

    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)
    painter = QPainter(pix)
    try:
        # Intentar usar fuente con soporte emoji en Windows
        font = QFont("Segoe UI Emoji", int(size * 0.85))
        painter.setFont(font)
        painter.drawText(pix.rect(), Qt.AlignCenter, emoji)
    finally:
        painter.end()

    pix.save(str(path), "PNG")
    return path


def get_stat_icon_path(key: str, emoji: str, size: int = 64) -> str:
    """Devuelve ruta del icono PNG para una estadística, generándolo si falta."""
    path = _icons_dir() / f"{key}.png"
    if not path.exists():
        path = _generate_emoji_icon(emoji, key, size=size)
    return str(path)