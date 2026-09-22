# TRUE VISION

TRUE VISION is a dark, local-first control center prototype that combines remote play, controller profiles, visual timing controls, and hardware diagnostics in one workspace.

## Included workspace

- **Overview** — session-ready Remote Play dashboard, system pulse, connected-device cards, and quick launch actions.
- **Profiles** — five independent profile slots with active-profile switching and local persistence.
- **Shot** — release timing, no-dip shots, dunk timing, meter smoothing, and tempo/timing controls.
- **Stabilizer** — response smoothing, deadzone, adaptive correction, mode, and polling controls.
- **Color / Meter** — meter visibility, color, appearance, and detection threshold in one place.
- **Hardware Dashboard** — native bridge status, controller bridge, controller/capture/Titan status cards, scan action, and Computer Vision Results log.
- **Remote Play** — preserved Remote Play session screen with quality, route, reconnect, and keyboard shortcut controls.
- **Controllers** — visual DualSense-style preview, editable Profile A mappings, and live keyboard input readout.
- **Auto Sync** — local-first profile replication state and recent activity.
- **Visual Backgrounds** — Shooting Stars, Shooting TRUE VISION, TRUE VISION Galaxy, Neon TRUE VISION, and Dark Particles.
- **Settings / About** — global preferences, build notes, roadmap, and the native-companion boundary.

## Run locally

This is a dependency-free static prototype. From this directory, run:

```bash
python3 -m http.server 4173
```

Then open <http://localhost:4173>.

## Product boundary

The browser build intentionally reports device state honestly. It does not claim to detect Windows HID devices, capture cards, Titan hardware, PSN sessions, virtual-controller bridges, or real video streams. The Hardware Dashboard explicitly shows **NATIVE BRIDGE NOT CONNECTED** until a desktop companion is installed.

The next production layer is a native companion service responsible for PS5/Xbox authentication and pairing, Remote Play streaming, controller polling, XInput/HID routing, capture-card or screen capture, continuous device monitoring, and Windows packaging. The browser UI is structured to become its front end without replacing the Remote Play workspace.

## Local behavior

Settings, mappings, active profile, and selected visual background persist through `localStorage`. Navigation, profile switching, reset actions, scan feedback, controller input readout, session controls, and results-log interactions are functional in the browser prototype.

## Files

- `index.html` — application structure and all views.
- `styles.css` — responsive dark neon / hardened mission-console visual system.
- `app.js` — navigation, local persistence, mock session behavior, profile controls, scan feedback, and controller interactions.
- `ZXVision_all_pages_latest.png` — original visual reference supplied with the repository.
