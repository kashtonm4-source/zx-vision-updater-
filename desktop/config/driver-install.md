# Windows driver notes

TRUE VISION does not bundle or silently install kernel drivers.

## ViGEmBus

Install ViGEmBus using its official signed Windows installer. The adapter in `true_vision/drivers/vigem.py` reports whether the native bridge is available and exposes explicit connect/disconnect boundaries for a future signed implementation.

## HidHide

Install HidHide using its official signed Windows installer. The adapter in `true_vision/drivers/hidhide.py` is read-only-by-default in this source tree and does not hide devices without an explicit future native configuration client.

The UI will show `NOT DETECTED`, `DISCONNECTED`, or a reason string when the drivers are absent. It will not manufacture a connected state.
