# TRUE VISION source tree

- `main.py` — desktop entry point.
- `true_vision/app.py` — Qt application bootstrap.
- `true_vision/models.py` — shot, stabilizer, meter, and profile data models.
- `true_vision/profiles.py` — five-profile persistence.
- `true_vision/logging_service.py` — timestamped local diagnostics.
- `true_vision/theme.py` — red/blue desktop theme.
- `true_vision/ui/` — dense dashboard, profile, shot, stabilizer, meter, Remote Play, and diagnostics pages.
- `true_vision/drivers/vigem.py` — ViGEmBus adapter boundary.
- `true_vision/drivers/hidhide.py` — HidHide adapter boundary.
- `true_vision/services/device_monitor.py` — controller/capture/Titan/driver status aggregation.
- `true_vision/services/remote_play.py` — Remote Play pairing/session boundary.
- `native/true_vision_launcher.c` — optional Windows bootstrapper source.
- `build_windows.ps1` — reproducible PyInstaller build.
- `tests/test_core.py` — profile persistence and no-fake-driver tests.
