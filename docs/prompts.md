# markview — prompts (with context & recap)

Every request that shaped `markview.html`, in chronological order. Each entry has:

- **Prompt** — the request as given.
- **Context** — where we were at that point (and any choices asked & answered).
- **Result** — what it produced.

Written so it is readable standalone: by you later, by others, and by an AI
without access to the original conversation.

---

## 1. Initial spec

**Prompt:** "markview : a name for a markdown files viewer which loads an `.md` files url e.g. from `href.hash` and renders it into html … in-page loading (ajax) without changing document … changing `href.hash` and re-rendering … single page, single html file that bundles all …"

**Context:** First message; the whole project was specified here. A design choice was asked & answered: which Markdown parser to bundle → **you chose "embed a mature library (marked) minified inline"** (not a hand-written parser).

**Result:** `markview.html` — single-file viewer: inline CSS + inlined `marked` v15 + app JS; hash routing; `.md` link interception.

---

## 2. Navbar

**Prompt:** "also add a text input for navbar-like"

**Context:** The core viewer existed; navigation was link-only.

**Result:** The address bar (`#path-input` + "Go"), kept in sync with the current file.

---

## 3. Sample docs

**Prompt:** "add sample md pages eg readme.md for this code and implementation explanations and a test page with image loading as external resource to load"

**Context:** Wanted landing/docs that exercise the viewer itself.

**Result:** `README.md`, `markview-explained.md`, `test-images.md` (external images).

---

## 4. Media URLs

**Prompt:** "ensure loading is fine from current document to target media url link (patch it)"

**Context:** Images/PDFs referenced relatively inside a note resolved against the viewer page, not the note's own folder.

**Result:** `rewriteRelativeUrls()` — relative media/`.md` URLs resolved against the current document's folder.

---

## 5. Upward links

**Prompt:** "does this work correctly for upward links eg `../README.md` from subdirectory document ?"

**Context:** A correctness question about `resolve`/`normalize`.

**Result:** Verified (unit + live tests) that `../`, `./`, and root-relative links resolve correctly; `..` above the root is safely clamped.

---

## 6. VS Code inner browser

**Prompt:** "test it in a inner browser of vscode"

**Context:** Wanted to preview inside VS Code rather than a system browser.

**Result:** Located the bundled Simple Browser / Integrated Browser; added `.vscode/launch.json` with `editor-browser` configs (F5).

---

## 7. Integrated browser docs

**Prompt:** "https://code.visualstudio.com/docs/debugtest/integrated-browser"

**Context:** You pointed at the docs for the newer Integrated Browser feature.

**Result:** Confirmed the `editor-browser` debug type and wired the launch configs accordingly.

---

## 8. Problems pane

**Prompt:** "fix markview as informed from 'Problems' pane"

**Context:** The inline script (minified `marked` UMD + plain JS) produced hundreds of false-positive TypeScript diagnostics in the Problems pane.

**Result:** `// @ts-nocheck` at the top of the inline script; verified "NO DIAGNOSTICS".

---

## 9. Mangled absolute URL

**Prompt:** "https://github.arkenidar.com/markview.html#https:/github.arkenidar.com/php_http_apps_todo/…"

**Context:** Typing a full `https://…` URL in the navbar was collapsing `https://` → `https:/` via `resolve()`.

**Result:** `isAbsoluteUrl()` + `toPath()` — same-origin URLs become their path; cross-origin `http(s)` open externally; `javascript:`/`data:` ignored.

---

## 10. Roadmap anchor

**Prompt:** "here roadmap hash does not have a patched behaviour https://github.arkenidar.com/markview.html#clay-js/README.md"

**Context:** `[Roadmap](#roadmap)` in `clay-js/README.md` — clicking it changed the hash to `#roadmap` (treated as a file path → 404), and headings had no `id`.

**Result:** `slugify()` + `addHeadingIds()`; `#anchor` clicks intercepted and scrolled.

---

## 11. Anchor back/forward

**Prompt:** "for this '#roadmap' link ( and alikes ) what about changing the URL to achieve back-button navigation also ?"

**Context:** Anchors scrolled but didn't change the URL, so Back/Forward couldn't revisit them.

**Result:** Nested hash `#path#anchor`, `parseHash()`, and a `hashchange` handler that distinguishes "same file, new anchor" (scroll) from "new file" (render).

---

## 12. fbclid cleanup

**Prompt:** "clean url removing 'fbclid' and keeping the rest intact https://github.arkenidar.com/markview.html?fbclid=…#clay-js/README.md#roadmap"

**Context:** Shared URLs carried tracking query params.

**Result:** `cleanUrl()` strips `fbclid`/`gclid`/`utm_*` etc. on load, keeping the hash and other params.

---

## 13. Scroll-to-top question

**Prompt:** "does navigating to a document that has no #hash make sure reading it scrolled from the top ? changing document and previous scrolling kept . do you confirm ?"

**Context:** A correctness question about scroll reset on document change.

**Result:** Confirmed (code + live test) that a document with no anchor always scrolls to the top.

---

## 14. Mobile LANGUAGE.md bug

**Prompt:** "try https://github.arkenidar.com/markview.html#clay-js/README.md#roadmap then https://github.arkenidar.com/LANGUAGE.md maybe in mobile the bug is there ( in Debian's Edge no bug , it is correct )"

**Context:** On mobile the `LANGUAGE.md` link navigated to root `LANGUAGE.md` (404) instead of `clay-js/LANGUAGE.md`.

**Result:** `.md` links resolved to root-relative paths at render time (robust even if `preventDefault` isn't honored).

---

## 15. Open integrated browser

**Prompt:** "open it in integrated-browser"

**Context:** Wanted the viewer open in VS Code's integrated browser.

**Result:** Confirmed the CLI can't launch it programmatically; documented F5 / Command Palette / Ctrl+Click paths.

---

## 16. Mobile scroll restoration

**Prompt:** "i see in my mobile screen with edge , that i go from readme.md to language.md and the scrolling is about at section 'program structure' and not the top of the document"

**Context:** Mobile browsers restore the previous scroll offset after the SPA swaps content.

**Result:** `history.scrollRestoration = 'manual'` + an early `window.scrollTo(0, 0)`.

---

## 17. Navbar shows full URL

**Prompt:** "note : in the #path-input element of document there is : 'clay-js/README.md' and not the more precise : 'clay-js/README.md#roadmap' like from eg URL of browser navigation"

**Context:** The address bar dropped the anchor.

**Result:** Navbar mirrors `path#anchor`; submit parses `path#anchor`; the navbar path is root-relative (so the displayed value round-trips).

---

## 18. Recap

**Prompt:** "racap"

**Context:** Asked for a summary of the whole project.

**Result:** Full recap of features, fixes, files, verification, and how to run.

---

## 19. Track the docs

**Prompt:** "update the .md documents and maybe add further documents for tracking all you explained to me"

**Context:** Wanted the docs to reflect the current code and to capture the journey.

**Result:** Refreshed `README.md`/`markview-explained.md`; added `markview-changelog.md` + `markview-testing.md`.

---

## 20. Photo gallery

**Prompt:** "add /home/arkenidar/Dropbox/000_tidy_this/my-notes/my-photos/ images in a /home/arkenidar/Dropbox/000_tidy_this/my-notes/my-photos/index.md"

**Context:** Wanted the 4 photos in `my-photos/` viewable in markview.

**Result:** `my-photos/index.md` gallery (personal, not part of this repo); images resolve to root-relative paths.

---

## 21. Link the gallery

**Prompt:** "ok"

**Context:** Follow-up to "want me to link the gallery from README?" — you said yes.

**Result:** Linked `my-photos/index.md` from `README.md` under a "Galleries" section (personal, not part of this repo).

---

## 22. Responsive layout

**Prompt:** "the layout is not responsive enough to manage narrow viewport without horizontal overflow , especially of navbar"

**Context:** Mobile viewports overflowed horizontally.

**Result:** `min-width: 0` on the navbar form, a ≤420px media query, `overflow-wrap: break-word`, and horizontal table scroll.

---

## 23. Docs + prompts list

**Prompt:** "update documentation and also list the prompts in a prompts.md file" + "also add … some brief context and recap … so … understandable ( also out of context )"

**Context:** Wanted the docs current and a standalone record of the prompts.

**Result:** This file (with Prompt / Context / Result), plus the doc updates above.

---

## 24. Scroll position memory

**Prompt:** "also as feature : when going back to a previous document ( browsed ) restore the previously saved page scroll position ( maybe saved before changing document 'forward' , change document 'backward' in navigation-history should re-apply it , restore it )"

**Context:** Back/forward restored the file but always scrolled to top; wanted per-document scroll memory.

**Result:** `scrollPositions` map — saves `window.scrollY` on leave, restores on return (anchor wins, first visit → top).

---

## 25. Problems pane — "Expression expected"

**Prompt:** (a VS Code diagnostic) `markview.html` line 95, "Expression expected", source javascript.

**Context:** A spurious syntax error reported by VS Code's HTML embedded-script validation at a multi-line template literal in the inlined `marked` library.

**Result:** Verified the JS is valid (TypeScript `parseDiagnostics` = 0); fixed with `.vscode/settings.json` → `"html.validate.scripts": false`.

---

## 26. Keep docs up-to-date

**Prompt:** "are you keeping up-to-date the documents of tech-documentation ?"

**Context:** Asked whether the `.md` docs reflect the latest code.

**Result:** Brought `README.md`, `markview-explained.md`, `markview-changelog.md`, `markview-testing.md`, and `prompts.md` up to date with the scroll-memory feature and the Problems-pane fix.

---

## 27. Prepare for publication

**Prompt:** "[publication] to prepare for publication use no more /home/arkenidar/Dropbox/000_tidy_this/my-notes , instead use the directory ~/code/mark-view for this mark-view gh repo ( ask for confirmations )"

**Context:** Wanted a clean repo separate from the notes folder.

**Result:** Created `~/code/mark-view` with `markview.html`, a clean `README.md`, `demo/`, `docs/`, `.vscode/`, `LICENSE` (MIT), and `.gitignore`; `git init` + initial commit.

---

## 28. Publish to GitHub

**Prompt:** "publish this repo as : public repo named arkenidar/mark-view"

**Context:** Ready to go public.

**Result:** Created the public repo https://github.com/arkenidar/mark-view and pushed `main`.

---

## 29. Update documentation

**Prompt:** "update documentation"

**Context:** Make the docs consistent with the published repo (neutralize personal-note references, reference the GitHub repo).

**Result:** Updated `docs/markview-changelog.md`, `docs/prompts.md`, `docs/markview-testing.md`, and `README.md`.
