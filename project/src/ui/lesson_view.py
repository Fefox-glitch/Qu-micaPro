from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTextBrowser, QScrollArea, QFrame,
                             QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.database import Database
from src.auth import AuthManager
from src.ui.quiz_view import QuizView

class LessonView(QWidget):
    def __init__(self, database: Database, auth_manager: AuthManager, lesson: dict, parent_view):
        super().__init__()
        self.db = database
        self.auth = auth_manager
        self.lesson = lesson
        self.parent_view = parent_view
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QWidget()
        header.setStyleSheet(
            "background-color: #1e3c72;"
            "padding: 16px;"
            "border-bottom: 2px solid #163056;"
        )
        header.setFixedHeight(96)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(40, 12, 40, 12)

        back_btn = QPushButton("← Volver")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: 2px solid white;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.go_back)

        title_label = QLabel(self.lesson['title'])
        font = QFont("Arial", 22)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: white;")
        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(8)
        title_shadow.setOffset(0, 1)
        title_label.setGraphicsEffect(title_shadow)

        header_layout.addWidget(back_btn)
        header_layout.addWidget(title_label, 1)

        header.setLayout(header_layout)

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(60, 40, 60, 40)
        content_layout.setSpacing(30)

        content_browser = QTextBrowser()
        html_content = self.lesson.get('content') or ''
        placeholder = html_content.strip() == '' or 'Contenido próximamente' in html_content
        if placeholder:
            module = None
            module_id = self.lesson.get('module_id')
            if module_id is not None:
                module = self.db.get_module_by_id(module_id)
            title = (module or {}).get('title', '')
            html_content = self._intro_html_for_module(title)
        content_browser.setHtml(html_content)
        content_browser.setStyleSheet("""
            QTextBrowser {
                border: none;
                background-color: white;
                font-size: 15px;
                line-height: 1.6;
            }
        """)
        content_browser.setOpenExternalLinks(False)
        content_browser.setMinimumHeight(400)

        content_layout.addWidget(content_browser)

        quiz_info_card = QFrame()
        quiz_info_card.setStyleSheet("""
            QFrame {
                background-color: #e3f2fd;
                border-left: 4px solid #2196F3;
                border-radius: 8px;
                padding: 20px;
            }
        """)

        quiz_info_layout = QVBoxLayout()

        quiz_title = QLabel("📝 Pon a prueba tus conocimientos")
        font = QFont("Arial", 16)
        font.setBold(True)
        quiz_title.setFont(font)
        quiz_title.setStyleSheet("color: #1e3c72;")

        quiz_description = QLabel("Completa el cuestionario para evaluar tu comprensión de esta lección.")
        quiz_description.setFont(QFont("Arial", 12))
        quiz_description.setStyleSheet("color: #666;")
        quiz_description.setWordWrap(True)

        start_quiz_btn = QPushButton("Iniciar Cuestionario")
        start_quiz_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        start_quiz_btn.setCursor(Qt.PointingHandCursor)
        start_quiz_btn.clicked.connect(self.start_quiz)

        quiz_info_layout.addWidget(quiz_title)
        quiz_info_layout.addWidget(quiz_description)
        quiz_info_layout.addSpacing(10)
        quiz_info_layout.addWidget(start_quiz_btn, alignment=Qt.AlignLeft)

        quiz_info_card.setLayout(quiz_info_layout)
        content_layout.addWidget(quiz_info_card)

        content_widget.setLayout(content_layout)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: white; }")

        layout.addWidget(header)
        layout.addWidget(scroll)

        self.setLayout(layout)

    def _intro_html_for_module(self, module_title: str) -> str:
        t = (module_title or '').lower()
        if 'conceptos básicos' in t:
            return (
                """
                <h2>¿Qué estudiarás en Conceptos Básicos?</h2>
                <p>Esta sección sienta las bases de la química. Verás qué es la materia, cómo se clasifica y cómo se mide.</p>
                <h3>Temas clave</h3>
                <ul>
                  <li>Estados de la materia y propiedades físicas</li>
                  <li>Átomos, elementos y compuestos</li>
                  <li>Unidades, magnitudes y conversiones</li>
                </ul>
                <p>Al terminar, tendrás el vocabulario y las herramientas para avanzar con seguridad.</p>
                """
            )
        if 'enlaces y compuestos' in t:
            return (
                """
                <h2>¿Qué estudiarás en Enlaces y Compuestos?</h2>
                <p>Aprenderás cómo se unen los átomos para formar sustancias y cómo esa unión determina sus propiedades.</p>
                <h3>Temas clave</h3>
                <ul>
                  <li>Enlace iónico vs. covalente</li>
                  <li>Polaridad y geometría molecular (VSEPR)</li>
                  <li>Estructuras de Lewis y nomenclatura básica</li>
                </ul>
                <p>Comprender estos conceptos te permitirá predecir comportamiento y reactividad de los compuestos.</p>
                """
            )
        if 'reacciones químicas' in t:
            return (
                """
                <h2>¿Qué estudiarás en Reacciones Químicas?</h2>
                <p>Verás cómo cambian las sustancias, cómo se representan las reacciones y cómo se cuantifican.</p>
                <h3>Temas clave</h3>
                <ul>
                  <li>Balanceo de ecuaciones químicas</li>
                  <li>Tipos de reacciones (síntesis, descomposición, etc.)</li>
                  <li>Estequiometría y rendimientos</li>
                </ul>
                <p>Dominarás el lenguaje de las reacciones y podrás resolver problemas de cantidad de materia.</p>
                """
            )
        if 'química avanzada' in t:
            return (
                """
                <h2>¿Qué estudiarás en Química Avanzada?</h2>
                <p>Profundizarás en modelos y teorías que explican fenómenos complejos y modernos.</p>
                <h3>Temas clave</h3>
                <ul>
                  <li>Termodinámica y equilibrio químico</li>
                  <li>Cinética y mecanismos de reacción</li>
                  <li>Química orgánica y materiales</li>
                </ul>
                <p>Esta sección te prepara para cursos superiores y aplicaciones reales.</p>
                """
            )
        return (
            """
            <h2>Introducción</h2>
            <p>Bienvenido. Aquí encontrarás una visión general del módulo y sus objetivos.</p>
            """
        )

    def start_quiz(self):
        lesson_id = self.lesson.get('id')
        quizzes = []
        if lesson_id:
            quizzes = self.db.get_quizzes_by_lesson(lesson_id)

        if not quizzes:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Sin Cuestionario", "Esta lección no tiene cuestionario disponible aún.")
            return

        quiz_view = QuizView(self.db, self.auth, self.lesson, quizzes, self.parent_view)
        parent = self.parent()

        if hasattr(parent, 'addWidget'):
            parent.addWidget(quiz_view)
            parent.setCurrentWidget(quiz_view)

    def go_back(self):
        self.parent_view.return_to_module()
