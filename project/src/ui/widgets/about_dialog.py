from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.ui.theme import Theme


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de QuímicaPro")
        self.setModal(True)
        self.setMinimumSize(420, 220)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("🧪 QuímicaPro")
        title_font = QFont("Arial", 18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)

        credit = QLabel("Desarrollado por Fernando Troncoso Ortiz · Fefox-Glitch · 2025")
        credit.setFont(QFont("Arial", 12))
        credit.setAlignment(Qt.AlignCenter)
        credit.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")

        note = QLabel("Aplicación educativa de química para estudiantes.")
        note.setFont(QFont("Arial", 11))
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")

        close_btn = QPushButton("Cerrar")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(
            "padding: 8px 16px; border-radius: 8px; background-color: #4CAF50; color: white; border: none;"
        )
        close_btn.clicked.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(credit)
        layout.addWidget(note)
        layout.addSpacing(6)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)