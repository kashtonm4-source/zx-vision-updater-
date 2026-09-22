import sys
from PySide6.QtWidgets import QApplication

from .logging_service import DiagnosticLog
from .profiles import ProfileStore
from .theme import APP_STYLE
from .ui.main_window import MainWindow

def run() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("TRUE VISION")
    app.setStyleSheet(APP_STYLE)
    window = MainWindow(ProfileStore(), DiagnosticLog())
    window.show()
    return app.exec()
