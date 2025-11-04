import sys
import logging
import traceback


def show_error(message: str, details: str | None = None) -> None:
    try:
        from PyQt5.QtWidgets import QMessageBox
        box = QMessageBox()
        box.setIcon(QMessageBox.Critical)
        box.setWindowTitle("Error")
        box.setText(message)
        if details:
            box.setDetailedText(details)
        box.exec_()
    except Exception:
        # Fallback a consola si PyQt no está disponible o falla el UI
        print(f"ERROR: {message}")
        if details:
            print(details)


def show_info(title: str, message: str) -> None:
    try:
        from PyQt5.QtWidgets import QMessageBox
        box = QMessageBox()
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle(title)
        box.setText(message)
        box.exec_()
    except Exception:
        print(f"INFO: {title} - {message}")


def show_warning(title: str, message: str) -> None:
    try:
        from PyQt5.QtWidgets import QMessageBox
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle(title)
        box.setText(message)
        box.exec_()
    except Exception:
        print(f"WARN: {title} - {message}")


def install_global_exception_hook() -> None:
    """Instala un excepthook global que registra y muestra errores críticos."""

    def _hook(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logging.error("Unhandled exception:\n%s", tb_str)
        show_error("Ocurrió un error inesperado. Por favor, intenta nuevamente.", tb_str)

    sys.excepthook = _hook