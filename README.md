# mark-view

A single-file, hash-driven **Markdown viewer**. It loads an `.md` file from the
URL hash (e.g. `markview.html#demo/sample.md`), renders it to HTML, and lets you
navigate to other `.md` files **without a page reload** — no build step, no
framework, no runtime dependencies.

Everything — the CSS, the `marked` parser, and the app logic — is bundled into
one `markview.html`. Drop it next to your `.md` files and serve the folder.

## Features

- **Hash routing** — `markview.html#path/to/file.md`; no hash → `index.md` → `README.md`.
- **In-page navigation** — `.md` links are intercepted and loaded via `fetch()`, no reload.
- **In-page anchors** — headings get auto `id`s; `#heading` links scroll and update the URL.
- **Back / forward** — nested hash `#path#anchor` steps through files *and* anchors.
- **Scroll memory** — restores the saved scroll position when you return to a document.
- **Address bar** — mirrors the full URL (`path#anchor`); accepts paths, `path#anchor`, bare `#anchor`, and absolute URLs.
- **Media support** — images/PDFs resolve relative to the current document's folder.
- **Responsive** — no horizontal overflow on narrow/mobile viewports.
- **URL cleanup** — strips `fbclid` / `gclid` / `utm_*` tracking params.
- **Self-contained** — one file, no CDN.

## Try it

Serve the folder and open `markview.html`:

```bash
python3 -m http.server 8000
# open http://localhost:8000/markview.html
```

- [Demo page](demo/sample.md)
- [Test page — external images](test-images.md)

## Documentation

- [Implementation explained](docs/markview-explained.md)
- [Changelog](docs/markview-changelog.md)
- [Testing & deployment](docs/markview-testing.md)
- [Prompts](docs/prompts.md)

## License

MIT — see [LICENSE](LICENSE). The bundled `marked` parser (v15) is also MIT.
