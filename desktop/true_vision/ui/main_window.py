from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QListWidget, QMainWindow, QPushButton, QStackedWidget, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget,
)

from ..drivers.hidhide import HidHideAdapter
from ..drivers.vigem import ViGEmBusAdapter
from ..logging_service import DiagnosticLog
from ..profiles import ProfileStore
from ..services.device_monitor import DeviceMonitor
from ..services.remote_play import RemotePlayService
from ..theme import APP_STYLE, BLUE, RED, mono
from .fields import add_number, add_slider

class MainWindow(QMainWindow):
    def __init__(self, store: ProfileStore, log: DiagnosticLog):
        super().__init__()
        self.store, self.log = store, log
        self.monitor = DeviceMonitor()
        self.remote = RemotePlayService()
        self.vigem, self.hidhide = ViGEmBusAdapter(), HidHideAdapter()
        self.setWindowTitle("TRUE VISION // Desktop Companion")
        self.resize(1440, 920)
        self.setStyleSheet(APP_STYLE)
        self._build()

    def _build(self):
        root = QWidget(); shell = QHBoxLayout(root); shell.setContentsMargins(18, 18, 18, 18); shell.setSpacing(18)
        sidebar = QFrame(); sidebar.setObjectName("panel"); side = QVBoxLayout(sidebar); side.setSpacing(8)
        logo = QLabel("TV  TRUE VISION\n     DESKTOP COMPANION"); logo.setStyleSheet(f"color:{RED.name()}; font-weight:700; font-size:16px;")
        side.addWidget(logo); side.addWidget(QLabel("CORE ENGINE"))
        self.sections = {}
        for name in ["Dashboard", "Profiles", "Shot", "Stabilizer", "Color / Meter", "Remote Play", "Diagnostics"]:
            button = QPushButton(name); self.sections[name] = button; side.addWidget(button)
        side.addStretch(); side.addWidget(QLabel("NATIVE STATUS")); self.native_label = QLabel("● BRIDGE NOT CONNECTED"); self.native_label.setStyleSheet(f"color:{RED.name()};")
        side.addWidget(self.native_label); shell.addWidget(sidebar, 0)
        self.stack = QStackedWidget(); shell.addWidget(self.stack, 1)
        pages = [self._dashboard(), self._profiles(), self._shot(), self._stabilizer(), self._meter(), self._remote(), self._diagnostics()]
        for page in pages: self.stack.addWidget(page)
        for index, name in enumerate(self.sections): self.sections[name].clicked.connect(lambda _=False, i=index: self.stack.setCurrentIndex(i))
        self.setCentralWidget(root)

    def _page(self, eyebrow: str, title: str, subtitle: str) -> tuple[QWidget, QVBoxLayout]:
        page = QWidget(); layout = QVBoxLayout(page)
        e = QLabel(eyebrow); e.setObjectName("eyebrow"); layout.addWidget(e)
        t = QLabel(title); t.setObjectName("title"); layout.addWidget(t)
        s = QLabel(subtitle); s.setStyleSheet("color:#8493a3; margin-bottom:12px;"); layout.addWidget(s)
        return page, layout

    def _panel(self, title: str) -> tuple[QFrame, QVBoxLayout]:
        panel = QFrame(); panel.setObjectName("panel"); layout = QVBoxLayout(panel); label = QLabel(title.upper()); label.setStyleSheet(f"color:{BLUE.name()}; font:10px 'Cascadia Mono'; letter-spacing:2px;"); layout.addWidget(label); return panel, layout

    def _dashboard(self):
        page, layout = self._page("SYSTEM / HARDWARE DASHBOARD", "Hardware dashboard", "Real device status, driver state, and reversible bridge controls.")
        scan = QPushButton("SCAN FOR DEVICES"); scan.setObjectName("primary"); scan.clicked.connect(self.scan_devices); layout.addWidget(scan, alignment=Qt.AlignRight)
        grid = QGridLayout()
        for i, (title, attr) in enumerate([("CONTROLLER BRIDGE", "controller"), ("CAPTURE SOURCE", "capture"), ("TITAN DEVICE", "titan"), ("VIGEMBUS + HIDHIDE", "drivers")]):
            panel, box = self._panel(title); label = QLabel("NOT DETECTED"); label.setStyleSheet(f"color:{RED.name()}; font-weight:700;"); setattr(self, f"status_{attr}", label); box.addWidget(label); box.addWidget(QLabel("Native bridge must be installed before a device can be reported as connected.")); grid.addWidget(panel, i // 2, i % 2)
        layout.addLayout(grid); bridge, b = self._panel("CONTROLLER BRIDGE"); self.bridge_label = QLabel("DISCONNECTED — no native virtual controller"); b.addWidget(self.bridge_label)
        row = QHBoxLayout(); connect = QPushButton("CONNECT"); connect.setObjectName("blue"); connect.clicked.connect(self.connect_bridge); disconnect = QPushButton("DISCONNECT"); disconnect.clicked.connect(self.disconnect_bridge); fix = QPushButton("HIDHIDE FIX"); fix.clicked.connect(self.fix_hidhide); row.addWidget(connect); row.addWidget(disconnect); row.addWidget(fix); b.addLayout(row); layout.addWidget(bridge); return page

    def _profiles(self):
        page, layout = self._page("CORE ENGINE / PROFILES", "Profiles", "Five independent configurations with persistent local storage.")
        self.profile_list = QListWidget(); self.profile_list.addItems([f"P{i + 1}  {p.name}" for i, p in enumerate(self.store.profiles)]); self.profile_list.currentRowChanged.connect(self.select_profile); self.profile_list.setCurrentRow(0); layout.addWidget(self.profile_list)
        save = QPushButton("SAVE ACTIVE PROFILE"); save.setObjectName("primary"); save.clicked.connect(lambda: (self.store.save(), self.write_log("Profile saved"))); layout.addWidget(save, alignment=Qt.AlignRight); return page

    def _shot(self):
        page, layout = self._page("CORE ENGINE / SHOT", "Shot timing", "Dense timing controls kept isolated to the active profile.")
        tabs = QTabWidget(); basic = QWidget(); form = QFormLayout(basic); profile = self.store.active().shot
        add_number(form, "Release Timing (%)", profile.release_timing, 0, 15); form.addRow("No Dip Shots", QCheckBox(checked=profile.no_dip_shots)); form.addRow("Dunk Timing", QComboBox()); form.addRow("Meter Action", QComboBox()); add_number(form, "Meter Smoothing", profile.meter_smoothing, 0, 100); form.addRow("Adaptive Timing", QCheckBox(checked=profile.adaptive_timing)); add_number(form, "Adaptive Window (ms)", profile.adaptive_window_ms, 0, 100)
        tabs.addTab(basic, "SHOT TIMING"); advanced = QWidget(); advanced_form = QFormLayout(advanced); add_number(advanced_form, "Release Offset (ms)", 0, -100, 100); add_number(advanced_form, "Input Buffer (ms)", 8, 0, 100); add_slider(advanced_form, "Confidence Threshold", 68); tabs.addTab(advanced, "ADVANCED"); layout.addWidget(tabs); return page

    def _stabilizer(self):
        page, layout = self._page("CORE ENGINE / STABILIZER", "Stabilizer", "All stabilizer settings from the reference workflow live in this category.")
        tabs = QTabWidget()
        for tab_name, fields in [("INPUT", [("Response Smoothing", 42), ("Deadzone", 4), ("Learning Rate", 18), ("Max Correction", 10)]), ("TARGET ROI", [("Target Height", 68), ("Target Width", 24), ("Vertical Offset", 0), ("Horizontal Offset", 0)]), ("ADAPTIVE", [("Adaptive Correction", 1), ("Stability Window", 32), ("Confidence Floor", 68), ("Recovery Speed", 24)])]:
            widget = QWidget(); form = QFormLayout(widget)
            for label, value in fields: add_slider(form, label, value, -100 if "Offset" in label else 0, 100)
            tabs.addTab(widget, tab_name)
        layout.addWidget(tabs); return page

    def _meter(self):
        page, layout = self._page("CORE ENGINE / COLOR + METER", "Color / Meter", "Meter visibility, color, appearance, and detection settings in one place.")
        panel, form = self._panel("METER CONTROLS"); controls = QFormLayout(); controls.addRow("Meter", QCheckBox(checked=True)); color = QComboBox(); color.addItems(["Signal Red", "Electric Blue", "Crimson", "Amber"]); controls.addRow("Meter Color", color); appearance = QComboBox(); appearance.addItems(["Minimal line", "Full bar", "Arc meter"]); controls.addRow("Appearance", appearance); add_slider(controls, "Detection Threshold", 68); add_slider(controls, "ROI Width", 24); add_slider(controls, "ROI Height", 68); controls.addRow("Show Confidence", QCheckBox(checked=True)); form.addLayout(controls); layout.addWidget(panel); return page

    def _remote(self):
        page, layout = self._page("REMOTE CONTROL / SESSION 01", "Remote Play", "The original Remote Play workspace remains inside the native companion.")
        panel, box = self._panel("REMOTE PLAY SESSION"); self.remote_label = QLabel("READY TO CONNECT — pairing requires the native console client"); box.addWidget(self.remote_label); row = QHBoxLayout(); start = QPushButton("START SESSION"); start.setObjectName("blue"); start.clicked.connect(self.start_remote); stop = QPushButton("END SESSION"); stop.clicked.connect(self.stop_remote); row.addWidget(start); row.addWidget(stop); box.addLayout(row); layout.addWidget(panel); return page

    def _diagnostics(self):
        page, layout = self._page("SYSTEM / DIAGNOSTICS", "Computer Vision Results", "Every meaningful local action is timestamped and copyable.")
        self.log_view = QTextEdit(); self.log_view.setReadOnly(True); self.log_view.setFont(mono()); layout.addWidget(self.log_view); clear = QPushButton("CLEAR LOG"); clear.clicked.connect(self.clear_log); layout.addWidget(clear, alignment=Qt.AlignRight); return page

    def write_log(self, message: str):
        line = self.log.write(message); self.log_view.append(line) if hasattr(self, "log_view") else None

    def scan_devices(self):
        result = self.monitor.scan(); self.status_controller.setText(result["controller"].upper()); self.status_capture.setText(result["capture"].upper()); self.status_titan.setText(result["titan"].upper()); self.status_drivers.setText(f"ViGEmBus: {result['vigembus'].reason} | HidHide: {result['hidhide'].reason}"); self.write_log("Device scan completed — no native devices reported")

    def connect_bridge(self):
        state = self.vigem.connect(); self.bridge_label.setText(f"{'CONNECTED' if state.connected else 'DISCONNECTED'} — {state.reason}"); self.write_log(f"Bridge connect requested — {state.reason}")

    def disconnect_bridge(self):
        self.vigem.disconnect(); self.bridge_label.setText("DISCONNECTED — user requested disconnect"); self.write_log("Bridge disconnected")

    def fix_hidhide(self):
        state = self.hidhide.fix(); self.write_log(f"HidHide fix requested — {state.reason}")

    def start_remote(self):
        state = self.remote.connect(); self.remote_label.setText(f"NOT CONNECTED — {state.reason}"); self.write_log(f"Remote Play start requested — {state.reason}")

    def stop_remote(self):
        self.remote.disconnect(); self.remote_label.setText("DISCONNECTED — session stopped"); self.write_log("Remote Play stopped")

    def select_profile(self, index: int):
        if index >= 0: self.store.select(index); self.write_log(f"Profile {index + 1} loaded")

    def clear_log(self):
        self.log.clear(); self.log_view.clear()
