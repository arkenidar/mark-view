# Test page — external images & navigation

This page exercises image loading from external URLs and in-page navigation.

## External images

![Random photo (picsum)](https://picsum.photos/seed/markview/800/400)

![Placeholder (placehold.co)](https://placehold.co/600x200?text=markview+placeholder)

### Linked image

[![Open picsum](https://picsum.photos/seed/markview2/400/200)](https://picsum.photos/)

## Navigation tests

- [Back to README](README.md) — relative `.md` link (in-page load, no reload)
- [Implementation explained](docs/markview-explained.md) — another `.md` link
- [External link example](https://example.com/) — should open normally

## What each item tests

- The images confirm **external resources load** and are constrained by
  `img { max-width: 100% }`.
- The `.md` links confirm **in-page navigation**.
- The external link confirms non-markdown links are left to the browser.
