# ZX Vision

ZX Vision is a dark, local-first remote-play control center prototype. It combines the product ideas behind console streaming clients, DualSense tooling, and XInput-style remapping in one focused workspace.

## Included in this prototype

- Remote Play dashboard with session-ready state, stream-quality controls, and connection metrics.
- Controller Studio with a visual DualSense-style input preview, keyboard input readout, and editable Profile A mappings.
- Auto Sync view showing local-first profile replication, paired devices, recent activity, and sync status.
- Settings for launch behavior, accent color, network discovery, relay fallback, and reduced motion.
- Responsive layout for desktop and smaller screens.
- Local persistence through `localStorage` for controller mappings and interface preferences.
- Keyboard shortcuts: `F1` opens Remote Play, `Esc` returns to Overview, and controller-like letter inputs update the input preview.

## Run locally

This is a dependency-free static prototype. From this directory, run any static server, for example:

```bash
python3 -m http.server 4173
```

Then open <http://localhost:4173>.

## Product boundary

The current build intentionally focuses on the interactive product shell and local state. It does not claim to implement a real PSN authentication flow, video codec pipeline, console pairing protocol, OS-level virtual-controller drivers, or gameplay input injection. Those capabilities belong in a native companion service with explicit platform permissions and security review; the browser prototype is ready to become its front end.

## Files

- `index.html` — application structure and views.
- `styles.css` — responsive dark neon visual system.
- `app.js` — navigation, local persistence, mock session behavior, and controller input interactions.
- `ZXVision_all_pages_latest.png` — original visual reference supplied with the repository.
