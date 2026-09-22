from dataclasses import dataclass
import platform

from .registry import DriverStatus

@dataclass
class HidHideState:
    installed: bool = False
    configured: bool = False
    reason: str = "Not initialized"

class HidHideAdapter:
    """Read-only-by-default HidHide integration boundary.

    A production bridge must use the official HidHide configuration client,
    request elevation explicitly, and provide a reversible restore operation.
    """
    def __init__(self):
        self.state = HidHideState()

    def status(self) -> DriverStatus:
        if platform.system() != "Windows":
            return DriverStatus("HidHide", False, False, "Windows-only device-hiding driver")
        return DriverStatus("HidHide", False, False, "Install HidHide and enable the native bridge")

    def fix(self) -> HidHideState:
        status = self.status()
        self.state = HidHideState(status.installed, False, status.reason if not status.available else "Ready to configure")
        return self.state

    def restore(self) -> HidHideState:
        self.state = HidHideState(self.state.installed, False, "HidHide configuration restored")
        return self.state
