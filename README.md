
## Native desktop companion source

The `desktop/` directory now contains a real multi-file PySide6 desktop companion source tree. It includes separate profile models, persistence, dense Shot/Stabilizer/Meter field groups, Remote Play service boundaries, diagnostic logging, device monitoring, ViGEmBus and HidHide adapters, a red/blue desktop theme, tests, a Windows launcher source, and a reproducible PyInstaller build script.

The supplied Vanta archive was inspected as a compiled distribution only. It contained `Vanta.exe`, Qt/OpenCV/FFmpeg runtime files, and `ViGEmClient.dll`, but no Python or UI source. TRUE VISION therefore uses its own implementation and does not copy opaque binaries. The driver adapters report missing Windows drivers honestly and never claim a virtual controller is connected when it is not.

On Windows, build the desktop executable with `desktop/build_windows.ps1`. The Linux sandbox cannot truthfully emit the final PyInstaller Windows executable because the Windows Python bootloader and Windows runtime APIs are required; the repository contains the source and reproducible build target for that `.exe`.
