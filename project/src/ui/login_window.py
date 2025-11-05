from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QStackedWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from src.auth import AuthManager
import re
from PyQt5.QtCore import QTimer
from src.ui.widgets.loading_overlay import LoadingOverlay

class LoginWindow(QWidget):
    login_successful = pyqtSignal()

    def __init__(self, auth_manager: AuthManager):
        super().__init__()
        self.auth_manager = auth_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QuímicaPro - Inicio de Sesión")
        self.setFixedSize(500, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #1e3c72, stop:1 #2a5298);
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #45a049;
            }
            QPushButton {
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton#primaryBtn {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#primaryBtn:hover {
                background-color: #45a049;
            }
            QPushButton#secondaryBtn {
                background-color: transparent;
                color: white;
                border: 2px solid white;
            }
            QPushButton#secondaryBtn:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(20)

        title_label = QLabel("🧪 QuímicaPro")
        font = QFont("Arial", 32)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)

        subtitle_label = QLabel("Aprende química de forma interactiva")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setAlignment(Qt.AlignCenter)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_login_page())
        self.stacked_widget.addWidget(self.create_register_page())

        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addSpacing(30)
        main_layout.addWidget(self.stacked_widget)

        footer_label = QLabel("Desarrollado por Fernando Troncoso Ortiz · Fefox-Glitch · 2025")
        footer_label.setFont(QFont("Arial", 10))
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: white;")
        main_layout.addSpacing(10)
        main_layout.addWidget(footer_label)

        self.setLayout(main_layout)
        self.loading_overlay = LoadingOverlay(self, text="Procesando…")

    def create_login_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        page_title = QLabel("Iniciar Sesión")
        font = QFont("Arial", 18)
        font.setBold(True)
        page_title.setFont(font)
        page_title.setAlignment(Qt.AlignCenter)

        self.login_username_input = QLineEdit()
        self.login_username_input.setPlaceholderText("Nombre de usuario")
        self.login_username_input.returnPressed.connect(self.handle_login)
        self.login_username_input.textChanged.connect(self.validate_login_form)

        self.login_error_label = QLabel("")
        self.login_error_label.setWordWrap(True)
        self.login_error_label.setStyleSheet("color: #ffdddd;")
        self.login_error_label.hide()

        self.login_processing_label = QLabel("Procesando…")
        self.login_processing_label.setStyleSheet("color: white; font-style: italic;")
        self.login_processing_label.hide()

        self.login_btn = QPushButton("Entrar")
        self.login_btn.setObjectName("primaryBtn")
        self.login_btn.clicked.connect(self.handle_login)
        self.login_btn.setCursor(Qt.PointingHandCursor)

        switch_btn = QPushButton("¿No tienes cuenta? Regístrate")
        switch_btn.setObjectName("secondaryBtn")
        switch_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        switch_btn.setCursor(Qt.PointingHandCursor)

        layout.addWidget(page_title)
        layout.addSpacing(20)
        layout.addWidget(self.login_username_input)
        layout.addWidget(self.login_error_label)
        layout.addWidget(self.login_processing_label)
        layout.addWidget(self.login_btn)
        layout.addSpacing(10)
        layout.addWidget(switch_btn)

        # Debounce para validación en login
        self.login_debounce_timer = QTimer(self)
        self.login_debounce_timer.setSingleShot(True)
        self.login_debounce_timer.setInterval(250)
        self.login_username_input.textChanged.connect(lambda: self.login_debounce_timer.start())
        self.login_debounce_timer.timeout.connect(self.validate_login_form)

        page.setLayout(layout)
        return page

    def create_register_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        page_title = QLabel("Crear Cuenta")
        font = QFont("Arial", 18)
        font.setBold(True)
        page_title.setFont(font)
        page_title.setAlignment(Qt.AlignCenter)

        self.register_username_input = QLineEdit()
        self.register_username_input.setPlaceholderText("Nombre de usuario")
        self.register_username_input.textChanged.connect(self.validate_register_form)

        self.register_display_name_input = QLineEdit()
        self.register_display_name_input.setPlaceholderText("Nombre para mostrar")
        self.register_display_name_input.returnPressed.connect(self.handle_register)
        self.register_display_name_input.textChanged.connect(self.validate_register_form)

        self.register_error_label = QLabel("")
        self.register_error_label.setWordWrap(True)
        self.register_error_label.setStyleSheet("color: #ffdddd;")
        self.register_error_label.hide()

        self.register_processing_label = QLabel("Procesando…")
        self.register_processing_label.setStyleSheet("color: white; font-style: italic;")
        self.register_processing_label.hide()

        self.register_btn = QPushButton("Registrarse")
        self.register_btn.setObjectName("primaryBtn")
        self.register_btn.clicked.connect(self.handle_register)
        self.register_btn.setCursor(Qt.PointingHandCursor)

        switch_btn = QPushButton("¿Ya tienes cuenta? Inicia sesión")
        switch_btn.setObjectName("secondaryBtn")
        switch_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        switch_btn.setCursor(Qt.PointingHandCursor)

        layout.addWidget(page_title)
        layout.addSpacing(20)
        layout.addWidget(self.register_username_input)
        layout.addWidget(self.register_display_name_input)
        layout.addWidget(self.register_error_label)
        layout.addWidget(self.register_processing_label)
        layout.addWidget(self.register_btn)
        layout.addSpacing(10)
        layout.addWidget(switch_btn)

        # Debounce para validación en registro
        self.register_debounce_timer = QTimer(self)
        self.register_debounce_timer.setSingleShot(True)
        self.register_debounce_timer.setInterval(250)
        self.register_username_input.textChanged.connect(lambda: self.register_debounce_timer.start())
        self.register_display_name_input.textChanged.connect(lambda: self.register_debounce_timer.start())
        self.register_debounce_timer.timeout.connect(self.validate_register_form)

        page.setLayout(layout)
        return page

    def handle_login(self):
        username = self.login_username_input.text().strip()
        error = self.validate_username(username)
        if error:
            self.login_error_label.setText(error)
            self.login_error_label.show()
            return
        self.start_processing_login()
        success, message = self.auth_manager.login(username)
        self.stop_processing_login()

        if success:
            self.login_successful.emit()
            self.close()
        else:
            QMessageBox.warning(self, "Error de inicio de sesión", message)

    def handle_register(self):
        username = self.register_username_input.text().strip()
        display_name = self.register_display_name_input.text().strip()

        error_user = self.validate_username(username)
        error_display = self.validate_display_name(display_name)
        if error_user or error_display:
            self.register_error_label.setText(error_user or error_display)
            self.register_error_label.show()
            return

        self.start_processing_register()
        success, message = self.auth_manager.register(username, display_name)
        self.stop_processing_register()

        if success:
            QMessageBox.information(self, "Éxito", "¡Cuenta creada exitosamente!")
            self.login_successful.emit()
            self.close()
        else:
            QMessageBox.warning(self, "Error de registro", message)

    def validate_username(self, username: str) -> str:
        if not username:
            return "Por favor ingresa tu nombre de usuario"
        if len(username) < 3:
            return "El nombre de usuario debe tener al menos 3 caracteres"
        if len(username) > 32:
            return "El nombre de usuario no puede exceder 32 caracteres"
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return "Usa solo letras, números y guiones bajos (sin espacios)"
        return ""

    def validate_display_name(self, display_name: str) -> str:
        if not display_name:
            return "Por favor ingresa un nombre para mostrar"
        if len(display_name) < 2:
            return "El nombre para mostrar debe tener al menos 2 caracteres"
        if len(display_name) > 50:
            return "El nombre para mostrar no puede exceder 50 caracteres"
        return ""

    def validate_login_form(self):
        error = self.validate_username(self.login_username_input.text().strip())
        if error:
            self.login_error_label.setText(error)
            self.login_error_label.show()
            self.login_btn.setEnabled(False)
        else:
            self.login_error_label.hide()
            self.login_btn.setEnabled(True)

    def validate_register_form(self):
        error_user = self.validate_username(self.register_username_input.text().strip())
        error_display = self.validate_display_name(self.register_display_name_input.text().strip())
        if error_user or error_display:
            self.register_error_label.setText(error_user or error_display)
            self.register_error_label.show()
            self.register_btn.setEnabled(False)
        else:
            self.register_error_label.hide()
            self.register_btn.setEnabled(True)

    def start_processing_login(self):
        self.login_btn.setEnabled(False)
        self.login_username_input.setEnabled(False)
        self.login_processing_label.show()
        self.loading_overlay.show_overlay()

    def stop_processing_login(self):
        self.login_processing_label.hide()
        self.login_username_input.setEnabled(True)
        self.login_btn.setEnabled(True)
        self.loading_overlay.hide_overlay()

    def start_processing_register(self):
        self.register_btn.setEnabled(False)
        self.register_username_input.setEnabled(False)
        self.register_display_name_input.setEnabled(False)
        self.register_processing_label.show()
        self.loading_overlay.show_overlay()

    def stop_processing_register(self):
        self.register_processing_label.hide()
        self.register_username_input.setEnabled(True)
        self.register_display_name_input.setEnabled(True)
        self.register_btn.setEnabled(True)
        self.loading_overlay.hide_overlay()
