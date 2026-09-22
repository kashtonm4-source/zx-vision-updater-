import json
from pathlib import Path
from typing import Callable

from .models import Profile, default_profiles

class ProfileStore:
    def __init__(self, root: Path | None = None):
        self.root = root or Path.home() / "AppData" / "Local" / "TrueVision"
        self.path = self.root / "profiles.json"
        self.profiles = self._load()
        self.active_index = 0
        self._listeners: list[Callable[[int], None]] = []

    def _load(self) -> list[Profile]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            loaded = [Profile.from_dict(item) for item in data]
            return loaded if len(loaded) == 5 else default_profiles()
        except (OSError, ValueError, TypeError):
            return default_profiles()

    def save(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps([profile.to_dict() for profile in self.profiles], indent=2), encoding="utf-8")

    def active(self) -> Profile:
        return self.profiles[self.active_index]

    def select(self, index: int) -> Profile:
        if not 0 <= index < len(self.profiles):
            raise IndexError("Profile index must be between 0 and 4")
        self.active_index = index
        for listener in self._listeners:
            listener(index)
        self.save()
        return self.active()

    def reset_active(self) -> None:
        name = self.active().name
        self.profiles[self.active_index] = Profile(name=name)
        self.save()

    def on_select(self, listener: Callable[[int], None]) -> None:
        self._listeners.append(listener)
