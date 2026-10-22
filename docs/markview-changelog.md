# markview — changelog

A record of the features and fixes added to `markview.html`, in order.

## Initial build

- Single-file viewer: inline CSS + inlined `marked` v15 + app JS.
- Hash routing (`#path/to/file.md`), `fetch()` + `marked.parse()` rendering.
- `.md` link interception (delegated click handler + `preventDefault`).
- Navbar address bar ("Go" button).

## Early fixes & samples

- **Relative media URLs** (`![x](pic.png)`) rewritten against the current
  document's folder (not the viewer page).
- **Upward links** (`../README.md`) verified correct via `resolve`/`normalize`.
- Sample docs: `README.md`, `markview-explained.md`, `test-images.md`.

## Absolute URL handling

- Bug: typing `https://…/readme.md` in the navbar mangled it (`https:` → `https:/`).
- Fix: `isAbsoluteUrl()` + `toPath()` — same-origin URLs become their path;
  cross-origin `http(s)` open in a new tab; `javascript:`/`data:` are ignored.

## In-page anchors

- Bug: `[Roadmap](#roadmap)` changed the hash to `#roadmap` (treated as a file
  path → 404), and headings had no `id`.
- Fix: `slugify()` + `addHeadingIds()` give headings `id`s; `#anchor` clicks are
  intercepted and scroll to the target.

## Anchor back/forward navigation

- Made anchors part of the URL: `#path#anchor`.
- `parseHash()` + `hashchange` distinguish "same file, new anchor" (scroll only)
  from "new file" (re-render). Back/Forward now steps through files *and* anchors.

## Tracking-param cleanup

- `cleanUrl()` strips `fbclid`/`gclid`/`utm_*` etc. from `?query` on load,
  keeping the hash and other params intact.

## Scroll restoration

- Bug (mobile): navigating to a document landed mid-page instead of the top.
- Fix: `history.scrollRestoration = 'manual'` plus an early `window.scrollTo(0, 0)`.

## Relative `.md` link robustness

- Bug (iOS Safari): default navigation on a relative `.md` link went to the
  wrong (root) path.
- Fix: `.md` links are resolved to root-relative paths at render time, so even a
  non-intercepted navigation lands on the correct file.

## Navbar shows the full URL

- The `#path-input` now displays `path#anchor` (mirroring the browser URL), and
  the submit handler parses `path#anchor`. The navbar path is root-relative, so
  the displayed value round-trips.

## Clean Problems pane

- `// @ts-nocheck` at the top of the inline script suppresses the hundreds of
  false-positive type diagnostics from the minified `marked` UMD and the
  plain-JS app code.

## Responsive layout

- Bug: narrow/mobile viewports had horizontal overflow, especially the navbar.
- Fix: `min-width: 0` on the navbar form, a ≤420px media query,
  `overflow-wrap: break-word` on `main`, and horizontal scrolling for wide tables.

## Docs & prompts

- Added `markview-changelog.md`, `markview-testing.md`, and `prompts.md`;
  refreshed `README.md` / `markview-explained.md`.
- (A personal photo gallery was also added in the author's notes — not part of
  this repo.)

## Scroll position memory

- Feature: going back to a previously-browsed document restores its saved scroll.
- A `scrollPositions` map saves `window.scrollY` on leave and re-applies it on
  return; explicit anchors still win, first visits start at top.

## Problems pane (embedded-script false positive)

- Bug: VS Code's HTML validator reported a spurious `Expression expected` at a
  multi-line template literal inside the inlined `marked` library.
- Fix: `.vscode/settings.json` with `"html.validate.scripts": false`.
