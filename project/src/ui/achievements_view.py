from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from src.database import Database
from src.auth import AuthManager
from src.ui.widgets.loading_overlay import LoadingOverlay
from src.ui.theme import Theme

class AchievementsView(QWidget):
    def __init__(self, database: Database, auth_manager: AuthManager):
        super().__init__()
        self.db = database
        self.auth = auth_manager
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        title_label = QLabel("Logros y Reconocimientos")
        font = QFont("Arial", 28)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")

        subtitle_label = QLabel("Desbloquea logros completando lecciones y obteniendo buenas puntuaciones")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")

        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)

        self.achievements_container = QWidget()
        self.achievements_layout = QGridLayout()
        self.achievements_layout.setSpacing(20)
        self.achievements_container.setLayout(self.achievements_layout)

        scroll = QScrollArea()
        scroll.setWidget(self.achievements_container)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(Theme.SCROLL_BORDERLESS)

        main_layout.addWidget(scroll)

        self.setLayout(main_layout)
        # Overlay de carga durante refrescos
        self.loading_overlay = LoadingOverlay(self, text="Cargando…")

    def refresh(self):
        self.loading_overlay.show_overlay()
        QTimer.singleShot(0, self._do_refresh)

    def _do_refresh(self):
        try:
            self.load_achievements()
        finally:
            self.loading_overlay.hide_overlay()

    def load_achievements(self):
        while self.achievements_layout.count():
            child = self.achievements_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        try:
            user_id = self.auth.get_current_user_id()
            all_achievements = self.db.get_all_achievements() or []
            user_achievements = self.db.get_user_achievements(user_id) or []
        except Exception:
            error_label = QLabel("Error al cargar logros")
            error_label.setStyleSheet("color: #c62828;")
            self.achievements_layout.addWidget(error_label, 0, 0)
            return

        earned_achievement_ids = {ua['achievement_id'] for ua in user_achievements}

        row = 0
        col = 0
        for achievement in all_achievements:
            is_earned = achievement.get('id') in earned_achievement_ids
            card = self.create_achievement_card(achievement, is_earned)
            self.achievements_layout.addWidget(card, row, col)

            col += 1
            if col >= 3:
                col = 0
                row += 1

    def create_achievement_card(self, achievement: dict, is_earned: bool) -> QFrame:
        card = QFrame()

        if is_earned:
            card.setStyleSheet(f"""
                QFrame {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 #FFD700, stop:1 #FFA500);
                    border-radius: {Theme.RADIUS_LG}px;
                    padding: 25px;
                    border: 3px solid {Theme.ACCENT};
                }}
            """)
        else:
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: #f5f5f5;
                    border: 2px solid {Theme.BORDER};
                    border-radius: {Theme.RADIUS_LG}px;
                    padding: 25px;
                }}
            """)

        card.setFixedHeight(220)

        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 14, 12, 14)
        layout.setAlignment(Qt.AlignCenter)

        icon_map = {
            'star': '⭐',
            'medal': '🥇',
            'trophy': '🏆',
            'award': '🎖️',
            'crown': '👑',
            'target': '🎯',
            'fire': '🔥'
        }

        icon = icon_map.get(achievement.get('icon', 'trophy'), '🏆')

        if not is_earned:
            icon = '🔒'

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 48))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setContentsMargins(0, 6, 0, 6)
        icon_label.setMinimumHeight(56)

        # ---------- PASTILLA DE LOGRO (mejorada) ----------
        badge = QLabel("🏅")
        badge.setAlignment(Qt.AlignCenter)
        badge.setFont(QFont("Arial", 11, QFont.Bold))

        # Tamaño y padding equilibrados
        badge.setFixedHeight(22)
        badge.setMinimumWidth(70)

        # Color y estilo según estado
        if is_earned:
            badge.setStyleSheet("""
                background-color: #FFC107;
                border-radius: 11px;
                padding: 2px 8px;
                color: #664400;
                border: 2px solid rgba(255,255,255,0.8);
            """)
        else:
            badge.setStyleSheet(f"""
                background-color: {Theme.BORDER};
                border-radius: 11px;
                padding: 2px 8px;
                color: {Theme.TEXT_MUTED};
                border: 2px solid rgba(255,255,255,0.2);
            """)

        badge.setText("🏅" if is_earned else "🔒")

        title_label = QLabel(achievement.get('title', '(Sin título)'))
        font = QFont("Arial", 14)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: white;" if is_earned else f"color: {Theme.TEXT_MUTED};")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)

        description_label = QLabel(achievement.get('description', ''))
        description_label.setFont(QFont("Arial", 11))
        description_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);" if is_earned else f"color: {Theme.TEXT_MUTED};")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        description_label.setContentsMargins(0, 4, 0, 0)

        if is_earned:
            status_label = QLabel("✓ Desbloqueado")
            font = QFont("Arial", 10)
            font.setBold(True)
            status_label.setFont(font)
            status_label.setStyleSheet("color: white;")
            status_label.setAlignment(Qt.AlignCenter)
        else:
            status_label = QLabel(self.get_requirement_text(achievement))
            status_label.setFont(QFont("Arial", 10))
            status_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
            status_label.setAlignment(Qt.AlignCenter)
            status_label.setWordWrap(True)

        layout.addWidget(icon_label)
        layout.addWidget(badge, alignment=Qt.AlignHCenter)
        layout.addSpacing(6)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addSpacing(5)
        layout.addWidget(status_label)

        card.setLayout(layout)
        return card

    def get_requirement_text(self, achievement: dict) -> str:
        req_type = achievement.get('requirement_type')
        req_value = achievement.get('requirement_value', 0)

        if req_type == 'lesson_complete':
            return f"Completa {req_value} lección{'es' if req_value > 1 else ''}"
        elif req_type == 'module_complete':
            modules = {1: 'Módulo 1', 2: 'Módulo 2', 3: 'Módulo 3', 4: 'Módulo 4'}
            return f"Completa el {modules.get(req_value, 'módulo')}"
        elif req_type == 'perfect_score':
            return f"Obtén {req_value}% en un quiz"
        elif req_type == 'streak':
            return f"Completa {req_value} lecciones seguidas"
        else:
            return "Requisito especial"
