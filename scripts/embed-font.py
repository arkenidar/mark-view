#!/usr/bin/env python3
"""Embed a monospace font subset into markview.html as a base64 @font-face.

Reproducible regeneration of the code / ASCII-art font. Tweak via env vars:

  MARKVIEW_FONT      path to the source TTF/OTF (default: system Noto Sans Mono)
  MARKVIEW_UNICODES  comma-separated unicode ranges (default: code + box art)

Requires: fontTools (pyftsubset) and brotli (for WOFF2).
"""
import base64
import os
import re
import subprocess
import sys
import tempfile

FONT = os.environ.get("MARKVIEW_FONT", "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf")
UNICODES = os.environ.get(
    "MARKVIEW_UNICODES",
    "U+0020-007E,U+00A0-00FF,U+2013-2014,U+2018-2019,U+201C-201D,U+2022,U+2026,U+20AC,"
    "U+2190-21FF,U+2500-257F,U+2580-259F,U+25A0-25FF",
)


def fail(msg):
    print("error:", msg, file=sys.stderr)
    sys.exit(1)


def subset_font(font, unicodes):
    if not os.path.exists(font):
        fail("font not found: %s" % font)
    fd, out = tempfile.mkstemp(suffix=".woff2")
    os.close(fd)
    try:
        subprocess.check_call(
            [
                "pyftsubset", font,
                "--unicodes=" + unicodes,
                "--output-file=" + out,
                "--flavor=woff2",
                "--no-hinting",
            ]
        )
        return open(out, "rb").read()
    except FileNotFoundError:
        fail("pyftsubset not found - install fonttools: pip install fonttools brotli")
    finally:
        if os.path.exists(out):
            os.unlink(out)


def main():
    data = subset_font(FONT, UNICODES)
    b64 = base64.b64encode(data).decode()

    html_path = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "markview.html")
    )
    if not os.path.exists(html_path):
        fail("markview.html not found at %s" % html_path)

    html = open(html_path, encoding="utf-8").read()
    new_url = "url(data:font/woff2;base64," + b64 + ")"
    html, n = re.subn(r"url\(data:font/woff2;base64,[A-Za-z0-9+/=]*\)", new_url, html, count=1)

    if n == 1:
        html = html
    else:
        rule = (
            '@font-face {\n'
            '  font-family: "markview-mono";\n'
            '  src: ' + new_url + ' format("woff2");\n'
            '  font-weight: 400;\n'
            '  font-style: normal;\n'
            '}\n'
        )
        anchor = "* { box-sizing: border-box; }"
        if anchor not in html:
            fail("could not find insertion point in markview.html")
        html = html.replace(anchor, rule + anchor, 1)

    open(html_path, "w", encoding="utf-8").write(html)
    print("embedded %d bytes (%d base64 chars) into %s" % (len(data), len(b64), html_path))
    print("font: %s" % FONT)
    print("unicodes: %s" % UNICODES)


if __name__ == "__main__":
    main()
