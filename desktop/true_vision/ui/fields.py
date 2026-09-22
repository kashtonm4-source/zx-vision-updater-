from PySide6.QtWidgets import QDoubleSpinBox, QFormLayout, QLabel, QSlider, QSpinBox, QWidget


def add_number(form: QFormLayout, label: str, value: float, minimum: float, maximum: float, step: float = 0.1):
    widget = QDoubleSpinBox()
    widget.setRange(minimum, maximum)
    widget.setSingleStep(step)
    widget.setValue(value)
    form.addRow(QLabel(label), widget)
    return widget


def add_integer(form: QFormLayout, label: str, value: int, minimum: int, maximum: int):
    widget = QSpinBox()
    widget.setRange(minimum, maximum)
    widget.setValue(value)
    form.addRow(QLabel(label), widget)
    return widget


def add_slider(form: QFormLayout, label: str, value: int, minimum: int = 0, maximum: int = 100):
    container = QWidget()
    slider = QSlider()
    slider.setOrientation(1)
    slider.setRange(minimum, maximum)
    slider.setValue(value)
    from PySide6.QtWidgets import QHBoxLayout
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(slider)
    form.addRow(QLabel(label), container)
    return slider
