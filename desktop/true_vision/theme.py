from PySide6.QtGui import QColor, QFont

RED = QColor("#ff5c67")
RED_DARK = QColor("#5a1f2b")
BLUE = QColor("#59b6ff")
BLUE_DARK = QColor("#14334a")
INK = QColor("#080b10")
PANEL = QColor("#111820")
TEXT = QColor("#f3f6fb")
MUTED = QColor("#8493a3")

APP_STYLE = f"""
QMainWindow, QWidget {{ background: {INK.name()}; color: {TEXT.name()}; font-family: 'Segoe UI'; }}
QLabel#eyebrow {{ color: {MUTED.name()}; font-size: 10px; letter-spacing: 2px; }}
QLabel#title {{ color: {TEXT.name()}; font-size: 26px; font-weight: 700; }}
QFrame#panel {{ background: {PANEL.name()}; border: 1px solid #263342; border-radius: 8px; }}
QFrame#alert {{ background: #23171d; border: 1px solid {RED.name()}; border-radius: 8px; }}
QPushButton {{ background: #172330; border: 1px solid #30475c; border-radius: 5px; padding: 9px 14px; color: {TEXT.name()}; }}
QPushButton:hover {{ border-color: {BLUE.name()}; background: {BLUE_DARK.name()}; }}
QPushButton#primary {{ background: {RED.name()}; border-color: {RED.name()}; color: #16090d; font-weight: 700; }}
QPushButton#primary:hover {{ background: #ff7a83; }}
QPushButton#blue {{ background: {BLUE.name()}; border-color: {BLUE.name()}; color: #07121c; font-weight: 700; }}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{ background: #0d131a; border: 1px solid #2b3b4b; border-radius: 4px; padding: 8px; color: {TEXT.name()}; }}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{ border-color: {BLUE.name()}; }}
QSlider::groove:horizontal {{ height: 5px; background: #273442; border-radius: 2px; }}
QSlider::handle:horizontal {{ width: 14px; margin: -5px 0; border-radius: 7px; background: {RED.name()}; }}
QListWidget {{ background: #0d131a; border: 1px solid #2b3b4b; border-radius: 5px; }}
QListWidget::item:selected {{ background: {BLUE_DARK.name()}; color: {BLUE.name()}; }}
QTabBar::tab {{ padding: 10px 14px; color: {MUTED.name()}; }}
QTabBar::tab:selected {{ color: {RED.name()}; border-bottom: 2px solid {RED.name()}; }}
"""

def mono(size: int = 10) -> QFont:
    font = QFont("Cascadia Mono", size)
    font.setStyleHint(QFont.Monospace)
    return font
