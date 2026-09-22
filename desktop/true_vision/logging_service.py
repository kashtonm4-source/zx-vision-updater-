from datetime import datetime
from pathlib import Path

class DiagnosticLog:
    def __init__(self, root: Path | None = None):
        self.root = root or Path.home() / "AppData" / "Local" / "TrueVision"
        self.path = self.root / "true_vision.log"
        self.entries: list[str] = []

    def write(self, message: str, level: str = "INFO") -> str:
        line = f"[{datetime.now():%H:%M:%S}] {level:<5} {message}"
        self.entries.append(line)
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
        except OSError:
            pass
        return line

    def clear(self) -> None:
        self.entries.clear()
        try:
            self.path.unlink(missing_ok=True)
        except OSError:
            pass
