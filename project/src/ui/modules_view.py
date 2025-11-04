from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QScrollArea, QListWidget,
                             QListWidgetItem, QStackedWidget)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from src.database import Database
from src.auth import AuthManager
from src.ui.lesson_view import LessonView
from src.ui.widgets.loading_overlay import LoadingOverlay
from src.ui.theme import Theme, lighten_color
from src.ui.icon_helper import display_icon_text

class ModulesView(QWidget):
    def __init__(self, database: Database, auth_manager: AuthManager):
        super().__init__()
        self.db = database
        self.auth = auth_manager
        self.current_module = None
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(300)
        self.sidebar.setStyleSheet("background-color: #f9f9f9; border-right: 1px solid #e0e0e0;")

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)

        title_label = QLabel("Módulos de Química")
        font = QFont("Arial", 18)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")

        sidebar_layout.addWidget(title_label)

        self.modules_list = QListWidget()
        self.modules_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
            }
            QListWidget::item {
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 5px;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
            }
            QListWidget::item:selected {
                background-color: #2196F3;
                color: white;
            }
        """)
        self.modules_list.itemClicked.connect(self.on_module_selected)

        sidebar_layout.addWidget(self.modules_list)
        self.sidebar.setLayout(sidebar_layout)

        self.content_stack = QStackedWidget()

        self.module_content_view = QWidget()
        self.lesson_view = None

        self.content_stack.addWidget(self.module_content_view)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack, 1)

        self.setLayout(main_layout)
        # Overlay de carga para refrescos y selección de módulo
        self.loading_overlay = LoadingOverlay(self, text="Cargando…")

    def refresh(self):
        self.loading_overlay.show_overlay()
        QTimer.singleShot(0, self._do_refresh)

    def _do_refresh(self):
        try:
            self.modules_list.clear()
            try:
                modules = self.db.get_all_modules() or []
            except Exception:
                error_item = QListWidgetItem("Error al cargar módulos")
                self.modules_list.addItem(error_item)
                return

            for module in modules:
                item = QListWidgetItem(f"{display_icon_text(module.get('icon'))}  {module.get('title','(Sin título)')}")
                item.setData(Qt.UserRole, module)
                font = QFont("Arial", 12)
                font.setBold(True)
                item.setFont(font)
                self.modules_list.addItem(item)

            if self.current_module:
                self.load_module_content(self.current_module)
        finally:
            self.loading_overlay.hide_overlay()

    def on_module_selected(self, item: QListWidgetItem):
        module = item.data(Qt.UserRole)
        self.current_module = module
        self.loading_overlay.show_overlay()
        QTimer.singleShot(0, lambda: self._load_module_safe(module))

    def _load_module_safe(self, module: dict):
        try:
            self.load_module_content(module)
        finally:
            self.loading_overlay.hide_overlay()

    def load_module_content(self, module: dict):
        while self.content_stack.count() > 1:
            widget = self.content_stack.widget(1)
            self.content_stack.removeWidget(widget)
            widget.deleteLater()

        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        header = QLabel(f"{display_icon_text(module.get('icon'))}  {module.get('title','(Sin título)')}")
        font = QFont("Arial", 24)
        font.setBold(True)
        header.setFont(font)
        header.setStyleSheet(f"color: {module.get('color', Theme.PRIMARY)};")

        description = QLabel(module.get('description', ''))
        description.setFont(QFont("Arial", 13))
        description.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
        description.setWordWrap(True)

        try:
            user_id = self.auth.get_current_user_id()
            completion = self.db.get_module_completion(user_id, module.get('id')) or {}
        except Exception:
            completion = {}

        completed = completion.get('completed', 0)
        total = completion.get('total', 0)
        percentage = completion.get('percentage', 0)
        progress_label = QLabel(f"Tu progreso: {completed}/{total} lecciones ({percentage}%)")
        font = QFont("Arial", 12)
        font.setBold(True)
        progress_label.setFont(font)
        progress_label.setStyleSheet("color: #4CAF50;")

        layout.addWidget(header)
        layout.addWidget(description)
        layout.addWidget(progress_label)

        lessons_label = QLabel("Lecciones Disponibles")
        font = QFont("Arial", 16)
        font.setBold(True)
        lessons_label.setFont(font)
        lessons_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; margin-top: 20px;")
        layout.addWidget(lessons_label)

        try:
            lessons = self.db.get_lessons_by_module(module.get('id')) or []
            progress_data = self.db.get_user_progress(user_id) or []
        except Exception:
            lessons = []
            progress_data = []

        # Filtrar la lección de prueba si existiera en BD
        def _is_test_lesson(l: dict) -> bool:
            t = (l.get('title','') or '').lower()
            return 'lección de prueba' in t or 'leccion de prueba' in t
        lessons = [l for l in lessons if not _is_test_lesson(l)]

        # Asegurar que haya una lección de introducción al inicio si no existe
        has_intro = any('introducción' in (l.get('title','').lower()) for l in lessons)
        if not has_intro:
            intro_lesson = {
                'id': f"virtual_intro_{module.get('id')}",
                'module_id': module.get('id'),
                'order_index': -1,
                'title': f"Introducción a {module.get('title','')}",
                'content': '',  # se rellenará con fallback en LessonView
                'estimated_minutes': 5,
                'is_virtual': True
            }
            lessons = [intro_lesson] + lessons
        completed_lesson_ids = {p['lesson_id'] for p in progress_data if p['completed']}

        for lesson in lessons:
            lesson_card = self.create_lesson_card(lesson, lesson['id'] in completed_lesson_ids)
            layout.addWidget(lesson_card)

        layout.addStretch()

        content_widget.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(Theme.SCROLL_BORDERLESS)

        self.content_stack.addWidget(scroll)
        self.content_stack.setCurrentIndex(1)

    def create_lesson_card(self, lesson: dict, is_completed: bool) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.CARD_BG};
                border: 2px solid {Theme.BORDER};
                border-radius: {Theme.RADIUS_MD}px;
                padding: 15px;
            }}
            QFrame:hover {{
                border: 2px solid {Theme.ACCENT};
            }}
        """)
        card.setFixedHeight(115)

        layout = QHBoxLayout()
        # Más aire entre elementos del card
        layout.setSpacing(16)
        layout.setContentsMargins(16, 10, 16, 10)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        # Pills de nombre de lección y duración
        nombre_leccion = lesson.get('title', 'Lección')
        duracion_texto = f"{lesson.get('estimated_minutes', 0)} minutos"

        meta_row = QHBoxLayout()
        meta_row.setContentsMargins(0, 0, 0, 0)
        meta_row.setSpacing(10)

        lesson_label = QLabel(f"📝 {nombre_leccion}")
        lesson_label.setFont(QFont("Arial", 11))
        lesson_label.setStyleSheet("""
            QLabel {
                background-color: #F7F9FC;
                border: 1px solid #DCE3EC;
                border-radius: 14px;
                padding: 6px 12px;
                color: #1A365D;
                font-weight: 600;
            }
            QLabel:hover {
                background-color: #EEF2FF;
                border-color: #BBD0FF;
            }
        """)
        lesson_label.setCursor(Qt.PointingHandCursor)

        duration_label = QLabel(f"⏱ {duracion_texto}")
        duration_label.setFont(QFont("Arial", 10))
        duration_label.setStyleSheet("""
            QLabel {
                background-color: #F0F4FF;
                border: 1px solid #C9D6FF;
                border-radius: 14px;
                padding: 6px 12px;
                color: #2C5282;
                font-weight: 500;
            }
            QLabel:hover {
                background-color: #E6EEFF;
                border-color: #B3C7FF;
            }
        """)
        duration_label.setCursor(Qt.PointingHandCursor)

        meta_row.addWidget(lesson_label)
        meta_row.addWidget(duration_label)
        meta_row.addStretch()

        left_layout.addLayout(meta_row)
        left_layout.addStretch()

        layout.addLayout(left_layout, 1)

        if is_completed:
            status_label = QLabel("✅ Completada")
            font = QFont("Arial", 11)
            font.setBold(True)
            status_label.setFont(font)
            status_label.setStyleSheet(f"color: {Theme.SUCCESS};")
            layout.addWidget(status_label)
            layout.setAlignment(status_label, Qt.AlignVCenter)

        start_btn = QPushButton("Comenzar" if not is_completed else "Repasar")
        start_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.ACCENT};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
        """)
        start_btn.setCursor(Qt.PointingHandCursor)
        start_btn.clicked.connect(lambda: self.start_lesson(lesson))

        layout.addWidget(start_btn)
        layout.setAlignment(start_btn, Qt.AlignVCenter)

        card.setLayout(layout)
        return card

    def start_lesson(self, lesson: dict):
        self.lesson_view = LessonView(self.db, self.auth, lesson, self)
        self.content_stack.addWidget(self.lesson_view)
        self.content_stack.setCurrentWidget(self.lesson_view)

    def return_to_module(self):
        if self.current_module:
            self.load_module_content(self.current_module)
