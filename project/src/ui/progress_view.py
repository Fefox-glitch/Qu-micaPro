from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QScrollArea, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap
from src.database import Database
from src.auth import AuthManager
from src.ui.widgets.loading_overlay import LoadingOverlay
from src.ui.theme import Theme, lighten_color
from src.ui.assets import get_stat_icon_path

class ProgressView(QWidget):
    def __init__(self, database: Database, auth_manager: AuthManager):
        super().__init__()
        self.db = database
        self.auth = auth_manager
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        title_label = QLabel("Mi Progreso")
        font = QFont("Arial", 28)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")

        subtitle_label = QLabel("Revisa tu avance en los módulos de química")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")

        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)

        self.stats_container = QWidget()
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(20)
        self.stats_container.setLayout(self.stats_layout)

        main_layout.addWidget(self.stats_container)

        modules_label = QLabel("Progreso por Módulo")
        font = QFont("Arial", 20)
        font.setBold(True)
        modules_label.setFont(font)
        modules_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; margin-top: 20px;")

        main_layout.addWidget(modules_label)

        self.modules_container = QWidget()
        self.modules_layout = QVBoxLayout()
        self.modules_layout.setSpacing(15)
        self.modules_container.setLayout(self.modules_layout)

        scroll = QScrollArea()
        scroll.setWidget(self.modules_container)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        main_layout.addWidget(scroll)

        self.setLayout(main_layout)
        # Overlay de carga para refrescos
        self.loading_overlay = LoadingOverlay(self, text="Cargando…")

    def refresh(self):
        self.loading_overlay.show_overlay()
        QTimer.singleShot(0, self._do_refresh)

    def _do_refresh(self):
        try:
            self.load_overall_stats()
            self.load_module_progress()
        finally:
            self.loading_overlay.hide_overlay()

    def load_overall_stats(self):
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

        avg_score = 0
        if progress:
            avg_score = sum(p['score'] for p in progress) // len(progress)

        try:
            modules = self.db.get_all_modules() or []
        except Exception:
            modules = []
        completed_modules = 0
        # Acumular lecciones para poder calcular porcentaje global
        lessons_completed_total = 0
        lessons_total = 0
        for module in modules:
            try:
                completion = self.db.get_module_completion(user_id, module.get('id')) or {}
            except Exception:
                completion = {}
            if completion['percentage'] == 100:
                completed_modules += 1
            # Sumar lecciones completadas y totales si están disponibles
            lessons_completed_total += completion.get('completed', 0)
            lessons_total += completion.get('total', 0)

        # Calcular porcentajes para cada estadística
        percent_modules = int((completed_modules / len(modules)) * 100) if len(modules) > 0 else 0
        percent_lessons = int((lessons_completed_total / lessons_total) * 100) if lessons_total > 0 else 0
        percent_score = int(avg_score)

        stats = [
            ("📚", "Módulos Completados", f"{completed_modules}/{len(modules)}", get_stat_icon_path("modules", "📚"), percent_modules),
            ("📖", "Lecciones Completadas", str(total_completed), get_stat_icon_path("lessons", "📖"), percent_lessons),
            ("⭐", "Puntuación Promedio", str(avg_score), get_stat_icon_path("avg_score", "⭐"), percent_score)
        ]

        for emoji, title, value, icon_path, percent in stats:
            stat_card = self.create_stat_card(emoji, title, value, icon_path=icon_path, percent=percent)
            self.stats_layout.addWidget(stat_card)

    def create_stat_card(self, emoji: str, title: str, value: str, icon_path: str = None, percent: int = None) -> QFrame:
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
        icon_box.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid {Theme.BORDER};
            }}
        """)

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

        # ---------- VALOR + PORCENTAJE ----------
        value_row = QHBoxLayout()
        value_row.setAlignment(Qt.AlignCenter)
        value_row.setSpacing(4)

        value_label = QLabel(str(value))
        font = QFont("Arial", Theme.FONT_STAT_VALUE)
        font.setBold(True)
        value_label.setFont(font)
        value_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")

        value_row.addWidget(value_label)

        if percent is not None:
            percent_label = QLabel(f"{percent}%")
            percent_label.setFont(QFont("Arial", Theme.FONT_BODY))
            percent_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
            value_row.addWidget(percent_label)

        # ---------- TÍTULO ----------
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", Theme.FONT_BODY))
        title_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
        title_label.setAlignment(Qt.AlignCenter)

        # ----------- ARMADO FINAL -----------
        layout.addWidget(icon_box, alignment=Qt.AlignCenter)
        layout.addLayout(value_row)
        layout.addWidget(title_label)
        layout.addStretch()

        card.setLayout(layout)
        return card

    def load_module_progress(self):
        while self.modules_layout.count():
            child = self.modules_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        try:
            user_id = self.auth.get_current_user_id()
            modules = self.db.get_all_modules() or []
        except Exception:
            modules = []

        for module in modules:
            try:
                completion = self.db.get_module_completion(user_id, module.get('id')) or {}
            except Exception:
                completion = {}
            card = self.create_module_progress_card(module, completion)
            self.modules_layout.addWidget(card)

    def create_module_progress_card(self, module: dict, completion: dict) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.CARD_BG};
                border: 2px solid {Theme.BORDER};
                border-radius: {Theme.RADIUS_MD}px;
                padding: 25px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        header_layout = QHBoxLayout()

        title_label = QLabel(f"{module['icon']}  {module['title']}")
        font = QFont("Arial", 16)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet(f"color: {module['color']};")

        percentage = completion.get('percentage', 0)
        status_label = QLabel("✅ Completado" if percentage == 100 else "🔄 En progreso")
        font = QFont("Arial", 12)
        font.setBold(True)
        status_label.setFont(font)
        status_label.setStyleSheet(f"color: {Theme.SUCCESS};" if percentage == 100 else f"color: {Theme.WARNING};")

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(status_label)

        completed = completion.get('completed', 0)
        total = completion.get('total', 0)
        progress_text = QLabel(f"{completed} de {total} lecciones completadas")
        progress_text.setFont(QFont("Arial", 12))
        progress_text.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")

        progress_bar = QProgressBar()
        progress_bar.setValue(percentage)
        progress_bar.setFixedHeight(25)
        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {Theme.BORDER};
                border-radius: 10px;
                text-align: center;
                background-color: #f5f5f5;
                font-weight: bold;
                font-size: 12px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 {module.get('color',Theme.PRIMARY)}, stop:1 {lighten_color(module.get('color',Theme.PRIMARY))});
                border-radius: 8px;
            }}
        """)

        layout.addLayout(header_layout)
        layout.addWidget(progress_text)
        layout.addWidget(progress_bar)

        card.setLayout(layout)
        return card
