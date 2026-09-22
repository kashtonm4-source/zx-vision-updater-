from dataclasses import dataclass

from ..drivers.hidhide import HidHideAdapter
from ..drivers.vigem import ViGEmBusAdapter

@dataclass
class DeviceSnapshot:
    controller: str = "Not detected"
    capture: str = "No signal"
    titan: str = "Not detected"

class DeviceMonitor:
    def __init__(self):
        self.vigem = ViGEmBusAdapter()
        self.hidhide = HidHideAdapter()
        self.snapshot = DeviceSnapshot()

    def scan(self) -> dict[str, object]:
        return {
            "controller": self.snapshot.controller,
            "capture": self.snapshot.capture,
            "titan": self.snapshot.titan,
            "vigembus": self.vigem.status(),
            "hidhide": self.hidhide.status(),
        }
