"""Builds the profile README visuals for github.com/HarshDubey23.

Same design as iamharshdubey.vercel.app: burgundy ground, bubblegum ink, one grotesk,
huge name split across two corners, project plates cut by a band at their midline.
All type is converted to outlines so GitHub shows exactly this, with no font loading.
Run: python3 build.py  (writes ./assets/*.svg)
"""
import base64
import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = pathlib.Path(__file__).parent
OUT = HERE / "assets"
OUT.mkdir(exist_ok=True)
IMG = HERE / "img"
FONTS = HERE / "fonts"

BG, SURF, BAND, INK, MUT, PAPER, SIG = "#14201a", "#1e2e25", "#0c140f", "#f6efdf", "#b4b09d", "#f6efdf", "#f4b23e"
EASE = 'calcMode="spline" keyTimes="0;1" keySplines="0.16 1 0.3 1"'


class Face:
    def __init__(self, file):
        self.f = TTFont(FONTS / file)
        self.gs = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm
        self.kern = self._kern()

    def _kern(self):
        pairs = {}
        try:
            lookups = self.f["GPOS"].table.LookupList.Lookup
        except KeyError:
            return pairs
        for lk in lookups:
            for st in lk.SubTable:
                if lk.LookupType == 9:
                    st = st.ExtSubTable
                if getattr(st, "LookupType", 2) != 2 or not hasattr(st, "Format"):
                    continue
                cov = st.Coverage.glyphs
                if st.Format == 1:
                    for i, g1 in enumerate(cov):
                        for pv in st.PairSet[i].PairValueRecord:
                            v = getattr(pv.Value1, "XAdvance", 0) if pv.Value1 else 0
                            if v:
                                pairs.setdefault((g1, pv.SecondGlyph), v)
                elif st.Format == 2:
                    c1 = st.ClassDef1.classDefs
                    c2 = st.ClassDef2.classDefs
                    self._cls = getattr(self, "_cls", [])
                    self._cls.append((set(cov), c1, c2, st.Class1Record))
        return pairs

    def kern_of(self, a, b):
        v = self.kern.get((a, b))
        if v is not None:
            return v
        for cov, c1, c2, recs in getattr(self, "_cls", []):
            if a in cov:
                r = recs[c1.get(a, 0)].Class2Record[c2.get(b, 0)]
                v = getattr(r.Value1, "XAdvance", 0) if r.Value1 else 0
                if v:
                    return v
        return 0

    def glyphs(self, text):
        return [self.cmap.get(ord(ch), self.cmap.get(ord("?"))) for ch in text]

    def width(self, text, size, track=0.0):
        g = self.glyphs(text)
        w = 0
        for i, n in enumerate(g):
            w += self.gs[n].width + (self.kern_of(n, g[i + 1]) if i + 1 < len(g) else 0)
        return w * size / self.upm + track * size * max(0, len(g) - 1)

    def path(self, text, size, x, y, track=0.0, anchor="start"):
        if anchor != "start":
            w = self.width(text, size, track)
            x -= w if anchor == "end" else w / 2
        s = size / self.upm
        pen = SVGPathPen(self.gs)
        g = self.glyphs(text)
        cx = 0.0
        for i, n in enumerate(g):
            tp = TransformPen(pen, (s, 0, 0, -s, x + cx, y))
            self.gs[n].draw(tp)
            cx += (self.gs[n].width + (self.kern_of(n, g[i + 1]) if i + 1 < len(g) else 0)) * s + track * size
        return pen.getCommands()


BLACK = Face("BG-Display.ttf")
BOLD = Face("BG-Head.ttf")
SEMI = Face("BG-Semi.ttf")
MED = Face("BG-Med.ttf")
REG = Face("BG-Reg.ttf")
MONO = Face("JB-Semi.ttf")


def t(face, text, size, x, y, fill=INK, track=0.0, anchor="start", extra=""):
    return f'<path fill="{fill}" d="{face.path(text, size, x, y, track, anchor)}"{extra}/>'


def wrap(face, text, size, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if face.width(trial, size) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def para(face, text, size, x, y, maxw, lh=1.38, fill=INK):
    out = []
    for i, line in enumerate(wrap(face, text, size, maxw)):
        out.append(t(face, line, size, x, y + i * size * lh, fill))
    return "".join(out), len(wrap(face, text, size, maxw))


def underline_link(face, text, size, x, y, fill=INK, anchor="start"):
    w = face.width(text, size)
    x0 = x - w if anchor == "end" else x
    return t(face, text, size, x0, y, fill) + f'<rect x="{x0:.1f}" y="{y + size * 0.22:.1f}" width="{w:.1f}" height="{max(2, size * 0.08):.1f}" fill="{fill}"/>'


def jpg(name):
    return "data:image/jpeg;base64," + base64.b64encode((IMG / name).read_bytes()).decode()


def _kt(delay, dur):
    """Delay folded into one animation that starts at 0, so the resting state is the finished one
    and a viewer that never runs the animation still shows everything."""
    total = delay + dur
    k = delay / total
    return total, f'0;{k:.3f};1', f'calcMode="spline" keySplines="0 0 1 1;0.16 1 0.3 1"'


def rise(inner, dy, delay, dur=1.1):
    total, kt, sp = _kt(delay, dur)
    return (f'<g>{inner}<animateTransform attributeName="transform" type="translate" values="0 {dy};0 {dy};0 0" keyTimes="{kt}" {sp} dur="{total:.2f}s" fill="freeze"/></g>')


def fade(inner, delay, dur=0.9, dy=18):
    total, kt, sp = _kt(delay, dur)
    return (f'<g>{inner}<animate attributeName="opacity" values="0;0;1" keyTimes="{kt}" dur="{total:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 {dy};0 {dy};0 0" keyTimes="{kt}" {sp} dur="{total:.2f}s" fill="freeze"/></g>')


def esc(x):
    return x.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<title>{esc(title)}</title>{body}</svg>')


def save(name, data):
    (OUT / name).write_text(data)
    print(f"{name:28s} {len(data) // 1024:5d} KB")


