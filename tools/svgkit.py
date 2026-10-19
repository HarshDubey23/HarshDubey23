"""Tiny SVG builder with measured text and per-file subset web fonts.

Every SVG embeds only the glyphs it actually uses, so animated cards stay small
enough for GitHub's image proxy while still rendering in real typefaces.
"""
import base64
import io
from xml.sax.saxutils import escape

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

import os
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + os.sep
FONTS = {
    "serif": "InstrumentSerif-Regular.ttf",
    "serifi": "InstrumentSerif-Italic.ttf",
    "sans": "InstrumentSans-Regular.ttf",
    "sansb": "InstrumentSans-Bold.ttf",
    "mono": "JetBrainsMono-Regular.ttf",
    "monob": "JetBrainsMono-Bold.ttf",
}
_loaded = {}


def font(key):
    if key not in _loaded:
        _loaded[key] = TTFont(FONT_DIR + FONTS[key])
    return _loaded[key]


def measure(text, key, size, ls=0.0):
    f = font(key)
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = f["head"].unitsPerEm
    w = 0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            raise ValueError(f"glyph {ch!r} missing in {key}")
        w += hmtx[g][0]
    return w * size / upm + ls * max(len(text) - 1, 0)


def wrap(text, key, size, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if measure(trial, key, size) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def _subset_b64(key, chars):
    f = TTFont(FONT_DIR + FONTS[key])
    opts = Options()
    opts.flavor = "woff"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    opts.notdef_outline = True
    sub = Subsetter(opts)
    sub.populate(text="".join(sorted(chars)) + " ")
    sub.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff"
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


class SVG:
    def __init__(self, w, h, title):
        self.w, self.h, self.title = w, h, title
        self.body = []
        self.defs = []
        self.css = []
        self.used = {}

    # --- primitives -------------------------------------------------------
    def add(self, s):
        self.body.append(s)

    def text(self, x, y, s, key, size, fill, anchor="start", ls=0, cls=None, extra=""):
        for ch in s:
            if ord(ch) not in font(key).getBestCmap():
                raise ValueError(f"glyph {ch!r} missing in {key} for {s!r}")
        self.used.setdefault(key, set()).update(s)
        c = f' class="{cls}"' if cls else ""
        lsa = f' letter-spacing="{ls}"' if ls else ""
        return (
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="f-{key}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" xml:space="preserve"{lsa}{c} {extra}>{escape(s)}</text>'
        )

    def t(self, *a, **k):
        self.add(self.text(*a, **k))

    def render(self):
        faces = []
        for key, chars in sorted(self.used.items()):
            faces.append(
                f"@font-face{{font-family:'f-{key}';src:url(data:font/woff;base64,"
                f"{_subset_b64(key, chars)}) format('woff');}}"
            )
        css = "\n".join(faces + self.css + [
            "@media (prefers-reduced-motion: reduce){*{animation:none!important;}}"
        ])
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.title)}">'
            f"<title>{escape(self.title)}</title>"
            f"<style>{css}</style><defs>{''.join(self.defs)}</defs>"
            + "".join(self.body)
            + "</svg>"
        )
