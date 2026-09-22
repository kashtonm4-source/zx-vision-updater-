from dataclasses import dataclass
import os
import platform
import shutil

@dataclass(frozen=True)
class DriverStatus:
    name: str
    installed: bool
    available: bool
    reason: str


def windows_only(name: str) -> DriverStatus:
    if platform.system() != "Windows":
        return DriverStatus(name, False, False, "Windows-only driver adapter; running outside Windows")
    return DriverStatus(name, False, False, "Adapter present; native verification not available in this build")


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def is_windows() -> bool:
    return os.name == "nt"
