from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QColor
from src.database import Database
from src.auth import AuthManager
from src.ui.widgets.loading_overlay import LoadingOverlay
from src.ui.theme import Theme, lighten_color
from src.ui.icon_helper import display_icon_text
from src.ui.assets import get_stat_icon_path

class HomeView(QWidget):
    def __init__(self, database: Database, auth_manager: AuthManager):
        super().__init__()
        self.db = database
        self.auth = auth_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        current_user = self.auth.get_current_user() or {}
        display_name = current_user.get('display_name') or "Estudiante"
        welcome_label = QLabel(f"¡Bienvenido, {display_name}!")
        font = QFont("Arial", 28)
        font.setBold(True)
        welcome_label.setFont(font)
        welcome_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")

        subtitle_label = QLabel("Continúa tu viaje de aprendizaje en química")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")

        layout.addWidget(welcome_label)
        layout.addWidget(subtitle_label)

        self.stats_container = QWidget()
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(20)
        self.stats_container.setLayout(self.stats_layout)

        layout.addWidget(self.stats_container)

        modules_section_label = QLabel("Módulos de Aprendizaje")
        font = QFont("Arial", 20)
        font.setBold(True)
        modules_section_label.setFont(font)
        modules_section_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; margin-top: 20px;")

        layout.addWidget(modules_section_label)

        self.modules_container = QWidget()
        self.modules_layout = QGridLayout()
        # Ordenar espaciado entre tarjetas/pastillas de módulos
        self.modules_layout.setContentsMargins(0, 0, 0, 0)
        # Más aire entre tarjetas/pastillas de módulos
        self.modules_layout.setHorizontalSpacing(32)
        self.modules_layout.setVerticalSpacing(32)
        self.modules_container.setLayout(self.modules_layout)

        layout.addWidget(self.modules_container)
        layout.addStretch()

        self.setLayout(layout)
        # Overlay de carga para operaciones de refresco
        self.loading_overlay = LoadingOverlay(self, text="Cargando…")
        # Lanzamos el primer refresco de forma diferida para que el overlay se pinte
        self.start_refresh()

    def start_refresh(self):
        self.loading_overlay.show_overlay()
        QTimer.singleShot(0, self.refresh)

    def refresh(self):
        try:
            self.load_stats()
            self.load_modules()
        finally:
            self.loading_overlay.hide_overlay()

    def load_stats(self):
        while self.stats_layout.count():
            child = self.stats_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        try:
            user_id = self.auth.get_current_user_id()
            progress = self.db.get_user_progress(user_id) or []
        except Exception:
            error_label = QLabel("Error al cargar estadísticas")
            error_label.setStyleSheet("color: #c62828;")
            self.stats_layout.addWidget(error_label)
            return

        total_completed = sum(1 for p in progress if p['completed'])

        try:
            achievements = self.db.get_user_achievements(user_id) or []
        except Exception:
            achievements = []
        total_achievements = len(achievements)

        avg_score = 0
        if progress:
            avg_score = sum(p['score'] for p in progress) // len(progress)

        stats = [
            ("📖", "Lecciones Completadas", str(total_completed), get_stat_icon_path("lessons", "📖")),
            ("🏆", "Logros Obtenidos", str(total_achievements), get_stat_icon_path("achievements", "🏆")),
            ("⭐", "Puntuación Promedio", f"{avg_score}%", get_stat_icon_path("avg_score", "⭐"))
        ]

        for emoji, title, value, icon_path in stats:
            stat_card = self.create_stat_card(emoji, title, value, icon_path=icon_path)
            self.stats_layout.addWidget(stat_card)

    def create_stat_card(self, emoji: str, title: str, value: str, icon_path: str = None) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.CARD_BG};
                border: 2px solid {Theme.BORDER};
                border-radius: {Theme.RADIUS_MD}px;
            }}
        """)
        card.setFixedHeight(210)

        layout = QVBoxLayout()
        layout.setSpacing(6)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setAlignment(Qt.AlignTop)

        # ---------- CONTENEDOR DEL ÍCONO (PASTILLA) ----------
        icon_box = QFrame()
        icon_box.setFixedSize(90, 60)
        icon_bg = "#ffffff" if Theme.MODE == "light" else lighten_color(Theme.CARD_BG, 0.12)
        icon_box.setStyleSheet(f"""
            QFrame {{
                background-color: {icon_bg};
                border-radius: 12px;
                border: 1px solid {Theme.BORDER};
            }}
        """)

        # Leve sombra para resaltar la pastilla
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 60))
        icon_box.setGraphicsEffect(shadow)

        icon_layout = QVBoxLayout(icon_box)
        icon_layout.setAlignment(Qt.AlignCenter)
        icon_layout.setContentsMargins(6, 6, 6, 6)

        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)

        if icon_path:
            pix = QPixmap(icon_path)
            if not pix.isNull():
                pix = pix.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(pix)
            else:
                icon_label.setText(emoji)
                icon_label.setFont(QFont("Arial", 32))
        else:
            icon_label.setText(emoji)
            icon_label.setFont(QFont("Arial", 32))

        icon_layout.addWidget(icon_label)

        # ---------- VALOR ----------
        value_label = QLabel(str(value))
        font = QFont("Arial", Theme.FONT_STAT_VALUE)
        font.setBold(True)
        value_label.setFont(font)
        value_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        value_label.setAlignment(Qt.AlignCenter)

        # ---------- TÍTULO ----------
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", Theme.FONT_BODY))
        title_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
        title_label.setAlignment(Qt.AlignCenter)

        # ----------- ARMADO FINAL -----------
        layout.addWidget(icon_box, alignment=Qt.AlignCenter)
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        layout.addStretch()

        card.setLayout(layout)
        return card

    def load_modules(self):
        while self.modules_layout.count():
            child = self.modules_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        try:
            modules = self.db.get_all_modules() or []
            user_id = self.auth.get_current_user_id()
        except Exception:
            error_label = QLabel("Error al cargar módulos")
            error_label.setStyleSheet("color: #c62828;")
            self.modules_layout.addWidget(error_label, 0, 0)
            return

        row = 0
        col = 0
        for module in modules:
            try:
                completion = self.db.get_module_completion(user_id, module['id']) or {}
            except Exception:
                completion = {}
            card = self.create_module_card(module, completion)
            self.modules_layout.addWidget(card, row, col)

            col += 1
            if col >= 2:
                col = 0
                row += 1

    def create_module_card(self, module: dict, completion: dict) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 {module['color']}, stop:1 {lighten_color(module['color'])});
                border-radius: {Theme.RADIUS_MD}px;
                padding: 20px;
            }}
        """)
        card.setFixedHeight(150)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 12, 10, 12)
        layout.setSpacing(8)

        # Mostrar ícono mapeado (atom/link/flask/beaker) como emoji
        title_label = QLabel(f"{display_icon_text(module.get('icon'))}  {module['title']}")
        font = QFont("Arial", 16)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: white;")

        desc_label = QLabel(module['description'])
        desc_label.setFont(QFont("Arial", Theme.FONT_BODY))
        desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        desc_label.setWordWrap(True)

        completed = completion.get('completed', 0)
        total = completion.get('total', 0)
        percentage = completion.get('percentage', 0)
        progress_label = QLabel(f"Progreso: {completed}/{total} ({percentage}%)")
        font = QFont("Arial", 11)
        font.setBold(True)
        progress_label.setFont(font)
        progress_label.setStyleSheet("color: white;")

        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addWidget(progress_label)

        card.setLayout(layout)
        return card
