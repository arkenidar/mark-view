# mark-view — how the single file is bundled

`markview.html` is self-contained: one HTML file, no runtime dependencies. It
bundles four things. This page explains each, how to regenerate it, and how to
tweak it.

## 1. CSS + app JavaScript

Hand-authored, inline in `<style>` and `<script>`. Edit directly in
`markview.html`.

## 2. `marked` (Markdown parser)

The minified `marked` UMD build (v15.0.12, MIT) is inlined verbatim inside the
`<script>`, right after the leading `// @ts-nocheck` comment. To update it:

```sh
curl -fsSL https://cdn.jsdelivr.net/npm/marked/marked.min.js -o /tmp/marked.min.js
# paste the new contents in place of the old marked block inside markview.html's <script>
```

The `// @ts-nocheck` stops the editor from type-checking the minified library
and the plain-JS app.

## 3. Embedded monospace font

A **Noto Sans Mono** subset (box-drawing, arrows, geometric shapes, block
elements, plus ASCII/Latin-1 and common punctuation — SIL OFL) is embedded as
a base64 WOFF2 `@font-face` named `markview-mono`, placed **first** in the code
font stack. This guarantees code blocks and ASCII/box art align identically on
every OS (Android included).

Regenerate it reproducibly:

```sh
python3 scripts/embed-font.py
```

Tweak it:

```sh
MARKVIEW_FONT=/path/to/another/monospace.ttf python3 scripts/embed-font.py
MARKVIEW_UNICODES="U+0020-007E,U+2500-257F" python3 scripts/embed-font.py
```

- `MARKVIEW_FONT` — source font (default: system Noto Sans Mono).
- `MARKVIEW_UNICODES` — glyph ranges to keep (default: code + box art).

Requires `fonttools` + `brotli`:

```sh
pip install fonttools brotli
```

## 4. `.vscode/` and settings

- `launch.json` — `editor-browser` debug configs (press **F5** to open markview
  in VS Code's integrated browser).
- `settings.json` — `"html.validate.scripts": false` (the inlined `marked` lib's
  multi-line template literals otherwise trigger a spurious "Expression expected").

## Philosophy

Everything ships as one file so it can be dropped next to any `.md` tree and
served (see `markview-testing.md`). The only generated parts are the inlined
`marked` lib and the embedded font subset — both reproducible as above.
