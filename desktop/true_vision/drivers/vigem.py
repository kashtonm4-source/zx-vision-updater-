from dataclasses import dataclass
import platform

from .registry import DriverStatus

@dataclass
class VirtualControllerState:
    connected: bool = False
    target: str = "Xbox 360"
    reason: str = "Not initialized"

class ViGEmBusAdapter:
    """Safe adapter boundary for ViGEmBus.

    This module does not ship or silently install ViGEmBus. A signed native
    implementation can replace the two explicit hooks on Windows.
    """
    def __init__(self):
        self.state = VirtualControllerState()

    def status(self) -> DriverStatus:
        if platform.system() != "Windows":
            return DriverStatus("ViGEmBus", False, False, "Windows-only virtual controller driver")
        return DriverStatus("ViGEmBus", False, False, "Install ViGEmBus and enable the native bridge")

    def connect(self, target: str = "Xbox 360") -> VirtualControllerState:
        status = self.status()
        if not status.available:
            self.state = VirtualControllerState(False, target, status.reason)
            return self.state
        self.state = VirtualControllerState(True, target, "Connected")
        return self.state

    def disconnect(self) -> VirtualControllerState:
        self.state = VirtualControllerState(False, self.state.target, "Disconnected by user")
        return self.state
