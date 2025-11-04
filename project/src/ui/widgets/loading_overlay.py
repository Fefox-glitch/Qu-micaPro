from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMovie


class LoadingOverlay(QWidget):
    def __init__(self, parent: QWidget, text: str = "Procesando…", spinner_gif: str = None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 120);")
        self._text = text
        self._spinner_gif = spinner_gif

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self._label = QLabel(self._text)
        self._label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(self._label)

        # Spinner opcional
        self._movie = None
        if self._spinner_gif:
            try:
                self._movie = QMovie(self._spinner_gif)
                if self._movie and self._movie.isValid():
                    spinner_label = QLabel()
                    spinner_label.setMovie(self._movie)
                    spinner_label.setAlignment(Qt.AlignCenter)
                    layout.addWidget(spinner_label)
                else:
                    self._movie = None
            except Exception:
                self._movie = None
        self.setLayout(layout)

        self.hide()
        # Mantener overlay redimensionado al padre
        if parent is not None:
            parent.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.parent() and event.type() in (QEvent.Resize, QEvent.Move):
            self._resize_to_parent()
        return super().eventFilter(obj, event)

    def _resize_to_parent(self):
        if self.parent() is not None:
            self.setGeometry(self.parent().rect())

    def show_overlay(self):
        self._resize_to_parent()
        if self._movie:
            self._movie.start()
        self.show()

    def hide_overlay(self):
        if self._movie:
            self._movie.stop()
        self.hide()