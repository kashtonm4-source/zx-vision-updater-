# TRUE VISION Desktop Companion

This folder is the native companion source for TRUE VISION. It is intentionally separate from the browser UI so Windows-only capabilities can be implemented and tested without pretending that a browser can enumerate HID devices or install drivers.

## Current native scope

The Python application provides a real desktop control surface with red/blue styling, five persistent profiles, dense Shot/Stabilizer/Meter fields, local diagnostics, Remote Play session state, and driver status adapters. ViGEmBus and HidHide are detected through Windows services/files/PowerShell only when available; the app never reports them as connected when they are not present.

## Windows setup

1. Install Python 3.11+ on Windows.
2. Install the optional dependencies with `py -m pip install -r requirements.txt`.
3. Install ViGEmBus and HidHide separately from their official installers if you need virtual-controller routing.
4. Start with `py main.py`.
5. Build a Windows executable with `powershell -ExecutionPolicy Bypass -File build_windows.ps1`.

The build script creates `dist/TrueVision/TrueVision.exe` with PyInstaller. This repository also includes `bin/TrueVisionLauncher.exe`, a real Windows GUI bootstrapper compiled from `native/true_vision_launcher.c`; it starts the Python companion and shows a Windows error dialog if Python is missing. A fully bundled PySide6 `.exe` still needs to be built on Windows because the Windows Python bootloader and runtime APIs are required.

## Important boundary

The adapter modules do not bypass driver security, hide devices by force, inject gameplay input, or claim real PS5/Xbox streaming. They expose explicit `available`, `installed`, and `reason` states for a future signed Windows service to use.
