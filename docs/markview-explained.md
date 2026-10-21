# markview — implementation explained

`markview.html` is one file with three inline parts:

1. **CSS** — a small stylesheet for the reader UI.
2. **`marked`** — the minified Markdown parser (v15.0.12, MIT), inlined verbatim.
3. **App script** — an IIFE that wires up routing, loading, navigation, and scrolling.

## URL scheme

The whole app state lives in the fragment:

```
#path/to/file.md            → file only (restore saved scroll, or top on first visit)
#path/to/file.md#roadmap    → file + in-page anchor
```

`parseHash()` splits it into `{ path, anchor }`:

```js
function parseHash() {
  var h = location.hash.replace(/^#/, '');
  if (!h) return { path: null, anchor: null };
  var i = h.indexOf('#');
  var path = i === -1 ? h : h.slice(0, i);
  var anchor = i === -1 ? null : h.slice(i + 1);
  // ... decodeURIComponent each part ...
  return { path: path || null, anchor: anchor || null };
}
```

## Path resolution

Links inside a page are relative to *that page's folder*, not the viewer's.
`resolve()` joins the link target onto the current file's directory and
normalizes `.` and `..`:

```js
function dirname(p) {
  var i = p.lastIndexOf('/');
  return i === -1 ? '' : p.slice(0, i);
}

function normalize(p) {
  var out = [];
  p.split('/').forEach(function (seg) {
    if (!seg || seg === '.') return;
    if (seg === '..') { out.pop(); return; }
    out.push(seg);
  });
  return out.join('/');
}

function resolve(base, href) {
  if (href.charAt(0) === '/') return normalize(href.slice(1)); // root-relative
  return normalize(dirname(base) + '/' + href);
}
```

So inside `design/foo.md`, `[other](other.md)` → `design/other.md`, and
`[top](../top.md)` → `top.md`.

## Load & render

`render()` reads the hash, fetches the file (`loadFirst` tries `index.md` then
`README.md` when there's no path), parses it with `marked.parse()`, and injects
it into `<main id="content">`. It then post-processes the DOM:

1. `rewriteRelativeUrls()` — resolves relative `img[src]`, media sources, and
   **`.md` links** to root-relative paths (so even a default browser navigation
   lands on the correct file).
2. `addHeadingIds()` — gives every heading a slug `id` (`## Roadmap` →
   `id="roadmap"`), with dedup.
3. `scrollToAnchor(anchor)` — scrolls to the anchor element, or to top.

## Navigation

`navigateTo(path, anchor)` builds `#path` or `#path#anchor`, syncs the address
bar, and sets `location.hash` (scrolling directly if the hash is unchanged):

```js
function navigateTo(path, anchor) {
  var hash = '#' + encodeURI(path);
  if (anchor) hash += '#' + anchor;
  pathInput.value = path + (anchor ? '#' + anchor : '');
  if (location.hash !== hash) location.hash = hash;
  else scrollToAnchor(anchor || null);
}
```

## Link interception

One delegated click handler on `#content`:

- `#anchor` → `navigateTo(currentFile, anchor)` (scrolls and updates the URL).
- absolute URL → same-origin `.md` is loaded in place (`toPath`); everything else is left to the browser.
- relative `.md` → `navigate(href)` (already root-relative after rewriting).

## Navbar

The submit handler splits the input on the first `#` into a path and an anchor,
then navigates. Paths are **root-relative** (matching the displayed URL); a bare
`#anchor` keeps the current file.

## Back / forward + scroll

```js
window.addEventListener('hashchange', function () {
  var parsed = parseHash();
  if (parsed.path && parsed.path === currentFile) {
    pathInput.value = parsed.path + (parsed.anchor ? '#' + parsed.anchor : '');
    scrollToAnchor(parsed.anchor);
  } else {
    if (currentFile) scrollPositions[currentFile] = window.scrollY; // save on leave
    render();
  }
});
```

`history.scrollRestoration = 'manual'` disables the browser's automatic scroll
restore. Instead, markview keeps a `scrollPositions` map: on leaving a document
it saves `window.scrollY`, and on returning it restores it (an explicit
`#anchor` still wins; first visits start at the top).

## URL cleanup

`cleanUrl()` runs once on load and strips tracking query params (`fbclid`,
`gclid`, `msclkid`, `mc_cid`, `mc_eid`, `igshid`, `_hsenc`, `_hsmi`, and the
`utm_*` family) via `URLSearchParams`, rewriting the URL with
`history.replaceState` — the hash is left intact.

## Responsive layout

A media query (≤ 420px) tightens the header spacing; the navbar form has
`min-width: 0` so the input can shrink; `main` uses `overflow-wrap:
break-word` so long URLs/code wrap instead of overflowing; and wide tables
scroll horizontally (`display: block; overflow-x: auto`).

## Bundling

`marked` is inlined as-is (MIT license header preserved), and a leading
`// @ts-nocheck` keeps the VS Code Problems pane quiet for the untyped inline
script. The whole app ships as one file with no build step and no runtime
network dependency.
