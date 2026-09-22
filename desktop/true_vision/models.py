from dataclasses import asdict, dataclass, field
from typing import Any

@dataclass
class StabilizerConfig:
    enabled: bool = True
    response_smoothing: float = 42.0
    deadzone: float = 3.5
    response_curve: str = "Balanced"
    adaptive_correction: bool = False
    target_height: float = 68.0
    target_width: float = 24.0
    vertical_offset: float = 0.0
    horizontal_offset: float = 0.0
    learning_rate: float = 18.0
    max_correction: float = 10.0

@dataclass
class ShotConfig:
    release_timing: float = 7.2
    no_dip_shots: bool = True
    dunk_timing: str = "Push & hold"
    meter_smoothing: float = 53.0
    meter_action: str = "Tempo"
    adaptive_timing: bool = False
    adaptive_window_ms: float = 18.0

@dataclass
class MeterConfig:
    enabled: bool = True
    color: str = "Signal Red"
    appearance: str = "Minimal line"
    detection_threshold: float = 68.0
    roi_width: float = 24.0
    roi_height: float = 68.0
    show_confidence: bool = True

@dataclass
class Profile:
    name: str
    shot: ShotConfig = field(default_factory=ShotConfig)
    stabilizer: StabilizerConfig = field(default_factory=StabilizerConfig)
    meter: MeterConfig = field(default_factory=MeterConfig)
    background: str = "Shooting Stars"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Profile":
        return cls(
            name=data.get("name", "Custom"),
            shot=ShotConfig(**data.get("shot", {})),
            stabilizer=StabilizerConfig(**data.get("stabilizer", {})),
            meter=MeterConfig(**data.get("meter", {})),
            background=data.get("background", "Shooting Stars"),
        )

def default_profiles() -> list[Profile]:
    names = ["Competitive", "Park / Casual", "Remote Play", "Practice Lab", "Custom"]
    return [Profile(name=name) for name in names]
