# markview — testing & deployment

## Serve locally

(`fetch()` is blocked under `file://`, so HTTP serving is required.)

- **htserve** (bundled in this repo, amd64):
  - GNU/Linux: `./htserve --port 8000`
  - Windows: `htserve.exe --port 8000`
- **Python** (built-in):
  - GNU/Linux/macOS: `python3 -m http.server 8000`
  - Windows: `python -m http.server 8000` (or `py -m http.server 8000`)

Then open `http://localhost:8000/markview.html`.

## Static checks

- `node --check` on the extracted inline script — syntax.
- VS Code's bundled TypeScript (`checkJs`) — expects "NO DIAGNOSTICS" thanks to
  `// @ts-nocheck`.
- `.vscode/settings.json` sets `"html.validate.scripts": false` (the inlined
  `marked` lib's multi-line template literals otherwise trigger a spurious
  "Expression expected").

## Headless browser tests

Used Chromium (desktop and mobile-emulated) for end-to-end checks:

- `--dump-dom` for rendering output.
- DevTools Protocol (CDP) for interaction: clicking links/anchors, typing in the
  navbar, and asserting `location.hash` / scroll / rendered content.
- Mobile emulation (`Emulation.setDeviceMetricsOverride` + touch + mobile UA) to
  check mobile behavior.
- Narrow-viewport overflow checks (320px / 360px: assert
  `scrollWidth === clientWidth`).

## VS Code integrated browser

- `.vscode/launch.json` has `editor-browser` configs — press **F5**.
- Or: Command Palette → "Browser: Open Integrated Browser" → paste the URL.
- Or: Ctrl+Click a `localhost` link in the terminal (opens in the integrated
  browser by default).

## Deployment

`markview.html` is a single file. Copy it next to your `.md` tree and serve the
folder.

- Repository: `https://github.com/arkenidar/mark-view`
- Live demo (author's server): `https://github.arkenidar.com/markview.html`

Re-deploy `markview.html` after changes to pick up the latest fixes.
