from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QStackedWidget, QLabel, QScrollArea, QProgressBar, QCheckBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from src.database import Database
from src.auth import AuthManager
from src.ui.home_view import HomeView
from src.ui.modules_view import ModulesView
from src.ui.progress_view import ProgressView
from src.ui.achievements_view import AchievementsView
from src.ui.widgets.loading_overlay import LoadingOverlay
from src.ui.widgets.about_dialog import AboutDialog
from src.ui.theme import Theme, lighten_color, set_mode

class MainWindow(QMainWindow):
    logout_requested = pyqtSignal()
    def __init__(self, database: Database, auth_manager: AuthManager):
        super().__init__()
        self.db = database
        self.auth = auth_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QuímicaPro - Plataforma de Aprendizaje")
        self.setMinimumSize(1200, 800)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton#navBtn {
                text-align: left;
                padding: 15px 20px;
                border: none;
                background-color: transparent;
                color: white;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton#navBtn:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton#navBtn:checked {
                background-color: #4CAF50;
            }
            QPushButton#logoutBtn {
                padding: 10px 20px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton#logoutBtn:hover {
                background-color: #da190b;
            }
        """)

        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Contenedor de contenido con barra de carga
        content_container = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0, 0)  # indeterminado
        self.loading_bar.setTextVisible(False)
        self.loading_bar.hide()
        self.loading_bar.setStyleSheet(
            f"QProgressBar {{ height: 4px; border: none; background: #eee; }}"
            f"QProgressBar::chunk {{ background-color: {Theme.SUCCESS}; }}"
        )

        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"background-color: {Theme.BACKGROUND};")

        self.home_view = HomeView(self.db, self.auth)
        self.modules_view = ModulesView(self.db, self.auth)
        self.progress_view = ProgressView(self.db, self.auth)
        self.achievements_view = AchievementsView(self.db, self.auth)

        self.content_stack.addWidget(self.home_view)
        self.content_stack.addWidget(self.modules_view)
        self.content_stack.addWidget(self.progress_view)
        self.content_stack.addWidget(self.achievements_view)

        content_layout.addWidget(self.loading_bar)
        content_layout.addWidget(self.content_stack, 1)

        footer_label = QLabel("Desarrollado por Fernando Troncoso Ortiz · Fefox-Glitch · 2025")
        footer_font = QFont("Arial", 10)
        footer_label.setFont(footer_font)
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; padding: 8px;")
        content_layout.addWidget(footer_label)
        content_container.setLayout(content_layout)

        self.loading_overlay = LoadingOverlay(content_container, text="Cargando…")

        main_layout.addWidget(content_container, 1)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.show_view(0)

    def create_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet(
            "QWidget {" +
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {Theme.PRIMARY}, stop:1 {lighten_color(Theme.PRIMARY, 0.25)});" +
            "}"
        )

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 20, 15, 20)

        app_title = QLabel("🧪 QuímicaPro")
        font = QFont("Arial", 20)
        font.setBold(True)
        app_title.setFont(font)
        app_title.setStyleSheet("color: white;")
        app_title.setAlignment(Qt.AlignCenter)

        user = self.auth.get_current_user()
        user_label = QLabel(f"👤 {user['display_name']}")
        user_label.setFont(QFont("Arial", 12))
        user_label.setStyleSheet("color: white; padding: 10px;")
        user_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(app_title)
        layout.addWidget(user_label)
        layout.addSpacing(20)

        # Switch de tema (Claro/Oscuro)
        theme_row = QHBoxLayout()
        theme_row.setSpacing(8)

        theme_label = QLabel("Tema")
        theme_label.setFont(QFont("Arial", 11))
        theme_label.setStyleSheet("color: white;")

        theme_switch = QCheckBox("Oscuro")
        theme_switch.setCursor(Qt.PointingHandCursor)
        theme_switch.setChecked(False)
        theme_switch.setStyleSheet("""
            QCheckBox { color: white; }
            QCheckBox::indicator { width: 42px; height: 22px; }
            QCheckBox::indicator:unchecked {
                border-radius: 11px;
                background: rgba(255,255,255,0.6);
            }
            QCheckBox::indicator:checked {
                border-radius: 11px;
                background: #2ecc71;
            }
        """)
        theme_switch.toggled.connect(self.on_theme_toggle)

        theme_row.addWidget(theme_label)
        theme_row.addStretch()
        theme_row.addWidget(theme_switch)
        layout.addLayout(theme_row)
        layout.addSpacing(10)

        self.home_btn = QPushButton("🏠  Inicio")
        self.home_btn.setObjectName("navBtn")
        self.home_btn.setCheckable(True)
        self.home_btn.setCursor(Qt.PointingHandCursor)
        self.home_btn.clicked.connect(lambda: self.show_view(0))

        self.modules_btn = QPushButton("📚  Módulos")
        self.modules_btn.setObjectName("navBtn")
        self.modules_btn.setCheckable(True)
        self.modules_btn.setCursor(Qt.PointingHandCursor)
        self.modules_btn.clicked.connect(lambda: self.show_view(1))

        self.progress_btn = QPushButton("📊  Mi Progreso")
        self.progress_btn.setObjectName("navBtn")
        self.progress_btn.setCheckable(True)
        self.progress_btn.setCursor(Qt.PointingHandCursor)
        self.progress_btn.clicked.connect(lambda: self.show_view(2))

        self.achievements_btn = QPushButton("🏆  Logros")
        self.achievements_btn.setObjectName("navBtn")
        self.achievements_btn.setCheckable(True)
        self.achievements_btn.setCursor(Qt.PointingHandCursor)
        self.achievements_btn.clicked.connect(lambda: self.show_view(3))

        self.nav_buttons = [self.home_btn, self.modules_btn, self.progress_btn, self.achievements_btn]

        for btn in self.nav_buttons:
            layout.addWidget(btn)

        layout.addStretch()

        about_btn = QPushButton("Acerca de QuímicaPro")
        about_btn.setObjectName("navBtn")
        about_btn.setCursor(Qt.PointingHandCursor)
        about_btn.clicked.connect(self.show_about_dialog)
        layout.addWidget(about_btn)

        logout_btn = QPushButton("Cerrar Sesión")
        logout_btn.setObjectName("logoutBtn")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.handle_logout)

        layout.addWidget(logout_btn)

        sidebar.setLayout(layout)
        self.sidebar = sidebar
        return sidebar

    def show_about_dialog(self):
        try:
            dlg = AboutDialog(self)
            dlg.exec_()
        except Exception:
            pass

    def on_theme_toggle(self, checked: bool):
        mode = "dark" if checked else "light"
        set_mode(mode)
        self.apply_theme()
        current = self.content_stack.currentIndex()
        self.show_view(current)

    def apply_theme(self):
        # Actualiza estilos base dependientes del tema
        self.content_stack.setStyleSheet(f"background-color: {Theme.BACKGROUND};")
        if hasattr(self, 'sidebar'):
            self.sidebar.setStyleSheet(
                "QWidget {" +
                f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
                f"stop:0 {Theme.PRIMARY}, stop:1 {lighten_color(Theme.PRIMARY, 0.25)});" +
                "}"
            )

    def show_view(self, index: int):
        for btn in self.nav_buttons:
            btn.setChecked(False)

        self.nav_buttons[index].setChecked(True)
        self.content_stack.setCurrentIndex(index)

        # Mostrar indicador y diferir la actualización para permitir refrescar UI
        self.start_loading()
        QTimer.singleShot(0, lambda: self._refresh_view(index))

    def _refresh_view(self, index: int):
        try:
            if index == 0:
                self.home_view.refresh()
            elif index == 1:
                self.modules_view.refresh()
            elif index == 2:
                self.progress_view.refresh()
            elif index == 3:
                self.achievements_view.refresh()
        finally:
            self.stop_loading()

    def start_loading(self):
        self.loading_bar.show()
        self.loading_overlay.show_overlay()

    def stop_loading(self):
        self.loading_bar.hide()
        self.loading_overlay.hide_overlay()

    def handle_logout(self):
        self.auth.logout()
        # Emitimos señal explícita para que la app muestre LoginWindow
        try:
            self.logout_requested.emit()
        finally:
            self.close()

    # Notificación desde vistas hijas cuando se otorga un logro
    def notify_achievement_awarded(self):
        try:
            # Si la pestaña de Logros está visible, refrescar inmediatamente
            if self.content_stack.currentIndex() == 3:
                self.achievements_view.refresh()
        except Exception:
            pass
