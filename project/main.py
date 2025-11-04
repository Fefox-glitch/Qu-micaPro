import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication
from src.database import Database
from src.auth import AuthManager
from src.ui.login_window import LoginWindow
from src.ui.main_window import MainWindow
from src.logging_config import setup_logging
from src.error_handler import install_global_exception_hook, show_error

def main():
    setup_logging()
    install_global_exception_hook()
    # El atributo de High DPI debe configurarse antes de crear QApplication
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    # Evita que la aplicación termine cuando se cierra la última ventana.
    # Así, al cerrar sesión desde MainWindow, podemos volver a mostrar LoginWindow.
    app.setQuitOnLastWindowClosed(False)

    try:
        db = Database()
    except RuntimeError as e:
        # Error de configuración .env u otros
        show_error("Error de configuración", str(e))
        return 1
    auth_manager = AuthManager(db)

    login_window = LoginWindow(auth_manager)

    def on_login_success():
        main_window = MainWindow(db, auth_manager)
        main_window.show()

        def on_main_window_closed(*args, **kwargs):
            nonlocal login_window
            login_window = LoginWindow(auth_manager)
            login_window.login_successful.connect(on_login_success)
            login_window.show()
            # Asegurar que la ventana de login tome foco y sea visible
            try:
                login_window.raise_()
                login_window.activateWindow()
            except Exception:
                pass

        # Escuchar tanto una señal específica de logout como la destrucción de la ventana
        main_window.logout_requested.connect(on_main_window_closed)
        main_window.destroyed.connect(on_main_window_closed)

    login_window.login_successful.connect(on_login_success)
    login_window.show()
    # Forzar visibilidad y foco por si el entorno la deja detrás
    try:
        login_window.raise_()
        login_window.activateWindow()
    except Exception:
        pass

    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
