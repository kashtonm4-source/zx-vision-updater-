from dataclasses import dataclass

@dataclass
class RemotePlayState:
    connected: bool = False
    console_name: str = "PlayStation 5"
    quality: str = "Auto — 1080p / 60 FPS"
    route: str = "Local network"
    reason: str = "Not connected"

class RemotePlayService:
    """Session state boundary for a future native console client."""
    def __init__(self):
        self.state = RemotePlayState()

    def connect(self, console_name: str = "PlayStation 5") -> RemotePlayState:
        self.state = RemotePlayState(False, console_name, self.state.quality, self.state.route, "Pairing requires the native console client")
        return self.state

    def disconnect(self) -> RemotePlayState:
        self.state = RemotePlayState(False, self.state.console_name, self.state.quality, self.state.route, "Disconnected")
        return self.state
