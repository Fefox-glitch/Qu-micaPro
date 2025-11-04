class Theme:
    MODE = "light"
    # Colors
    PRIMARY = "#1e3c72"
    ACCENT = "#2196F3"
    SUCCESS = "#4CAF50"
    WARNING = "#FF9800"
    DANGER = "#c62828"
    TEXT_PRIMARY = "#1e3c72"
    TEXT_SECONDARY = "#666"
    TEXT_MUTED = "#aaa"
    CARD_BG = "#ffffff"
    BORDER = "#e0e0e0"
    BACKGROUND = "#ffffff"
    SCROLL_BORDERLESS = "QScrollArea { border: none; }"

    # Metrics
    RADIUS_SM = 8
    RADIUS_MD = 12
    RADIUS_LG = 15

    SPACING_XS = 4
    SPACING_SM = 8
    SPACING_MD = 12
    SPACING_LG = 20

    # Font sizes
    FONT_H1 = 28
    FONT_H2 = 20
    FONT_H3 = 16
    FONT_BODY = 11
    FONT_STAT_VALUE = 24
    FONT_EMOJI = 32


def lighten_color(hex_color: str, factor: float = 0.2) -> str:
    """Lighten a HEX color by a given factor (0-1)."""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = min(255, int(r * (1 + factor)))
    g = min(255, int(g * (1 + factor)))
    b = min(255, int(b * (1 + factor)))
    return f'#{r:02x}{g:02x}{b:02x}'


def _apply_light_palette():
    Theme.MODE = "light"
    Theme.PRIMARY = "#1e3c72"
    Theme.ACCENT = "#2196F3"
    Theme.SUCCESS = "#4CAF50"
    Theme.WARNING = "#FF9800"
    Theme.DANGER = "#c62828"
    Theme.TEXT_PRIMARY = "#1e3c72"
    Theme.TEXT_SECONDARY = "#666"
    Theme.TEXT_MUTED = "#aaa"
    Theme.CARD_BG = "#ffffff"
    Theme.BORDER = "#e0e0e0"
    Theme.BACKGROUND = "#ffffff"


def _apply_dark_palette():
    Theme.MODE = "dark"
    # Paleta afinada para alta legibilidad y contraste en modo oscuro
    Theme.PRIMARY = "#1e3c72"   # azul profundo para sidebar y acentos
    Theme.ACCENT = "#3b82f6"    # acento principal (links/botones)
    Theme.SUCCESS = "#22c55e"
    Theme.WARNING = "#f59e0b"
    Theme.DANGER = "#ef4444"
    Theme.TEXT_PRIMARY = "#e6edf3"
    Theme.TEXT_SECONDARY = "#9aa4ad"
    Theme.TEXT_MUTED = "#7b818a"
    Theme.CARD_BG = "#1a1f25"   # paneles y tarjetas
    Theme.BORDER = "#2a3139"
    Theme.BACKGROUND = "#0d1117"  # fondo general


def set_mode(mode: str):
    mode = (mode or "light").lower()
    if mode == "dark":
        _apply_dark_palette()
    else:
        _apply_light_palette()