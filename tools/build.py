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
OUT = HERE.parent / "assets"
OUT.mkdir(exist_ok=True)
IMG = HERE / "img"
FONTS = pathlib.Path("/usr/share/fonts/opentype/inter")  # Inter Display; point this at your copy

BG, SURF, BAND, INK, MUT, PAPER = "#3d0012", "#4d0519", "#30000e", "#ff99d3", "#e2a3c4", "#ffe1f0"
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


BLACK = Face("InterDisplay-ExtraBold.otf")
BOLD = Face("InterDisplay-Bold.otf")
SEMI = Face("Inter-SemiBold.otf")
MED = Face("Inter-Medium.otf")
REG = Face("Inter-Regular.otf")


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


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1280, 800
    FX, FW, FH = 960, 320, 620
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<rect x="{FX}" width="{FW}" height="{FH}" fill="{INK}"/>',
         f'<rect x="{FX}" y="{FH}" width="{FW}" height="{H - FH}" fill="{BAND}"/>']
    # the twin: the 3D face on the site, drawn flat. It blinks, looks around and talks.
    cx, cy, r = FX + FW / 2, 330, 104
    eyes = "".join(
        f'<rect x="{cx + dx - 11}" y="{cy - 34}" width="22" height="40" rx="11" fill="{INK}">'
        f'<animate attributeName="height" values="40;40;4;40;40" keyTimes="0;0.9;0.94;0.98;1" dur="4.6s" repeatCount="indefinite"/>'
        f'<animate attributeName="y" values="{cy - 34};{cy - 34};{cy - 16};{cy - 34};{cy - 34}" keyTimes="0;0.9;0.94;0.98;1" dur="4.6s" repeatCount="indefinite"/></rect>'
        for dx in (-34, 34))
    mouth = (f'<rect x="{cx - 22}" y="{cy + 34}" width="44" height="8" rx="4" fill="{INK}">'
             f'<animate attributeName="height" values="8;22;10;18;6;20;8;8" keyTimes="0;0.08;0.16;0.26;0.36;0.46;0.56;1" dur="3.2s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{cy + 34};{cy + 27};{cy + 33};{cy + 29};{cy + 35};{cy + 28};{cy + 34};{cy + 34}" keyTimes="0;0.08;0.16;0.26;0.36;0.46;0.56;1" dur="3.2s" repeatCount="indefinite"/></rect>')
    look = (f'<g><circle cx="{cx}" cy="{cy}" r="{r}" fill="{BG}"/>'
            f'<g>{eyes}{mouth}<animateTransform attributeName="transform" type="translate" values="0 0;10 -4;10 -4;-12 2;-12 2;0 0;0 0" keyTimes="0;0.12;0.38;0.5;0.76;0.88;1" dur="7s" repeatCount="indefinite"/></g>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" dur="5s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></g>')
    b.append(fade(look, 0.5, 1.2, 24))
    b.append(t(SEMI, "This is my AI twin. It talks.", 19, FX + 26, 50, BG))
    b.append(underline_link(SEMI, "Ask it anything on my site", 19, FX + 26, 80, BG))
    b.append(fade(t(MED, "It answers from my real projects,", 17, FX + 26, FH - 58, BG)
                  + t(MED, "in voice, and opens the right case.", 17, FX + 26, FH - 34, BG), 1.4))
    # the name, split to two corners
    b.append(f'<clipPath id="c1"><rect x="0" y="0" width="{FX}" height="200"/></clipPath>')
    b.append(f'<g clip-path="url(#c1)">{rise(t(BLACK, "Harsh", 196, 30, 176, INK, -0.05), 200, 0.1)}</g>')
    b.append(f'<clipPath id="c2"><rect x="0" y="{FH}" width="{W}" height="{H - FH}"/></clipPath>')
    b.append(f'<g clip-path="url(#c2)">{rise(t(BLACK, "Dubey", 196, W - 36, H - 26, INK, -0.05, "end"), 200, 0.28)}</g>')
    # statement
    lines = ["I build AI agents that can't be", "talked into the wrong action, and I", "measure everything I ship."]
    st = "".join(t(MED, ln, 38, 240, 390 + i * 50, INK, -0.01) for i, ln in enumerate(lines))
    sub = (t(REG, "ML engineer and B.Tech AI & ML student at KIET,", 23, 240, 566, MUT)
           + t(REG, "Delhi NCR. Looking for internships in 2026.", 23, 240, 598, MUT))
    b.append(fade(st, 0.55))
    b.append(fade(sub, 0.7))
    label = "iamharshdubey.vercel.app"
    lw = SEMI.width(label, 22) + 56
    b.append(fade(f'<rect x="240" y="636" width="{lw:.0f}" height="56" rx="28" fill="{INK}"/>'
                  + t(SEMI, label, 22, 268, 672, BG) , 0.85))
    return svg(W, H, "".join(b), "Harsh Dubey. I build AI agents that can't be talked into the wrong action, and I measure everything I ship.")


# ---------------------------------------------------------------- project plates
PROJECTS = [
    dict(slug="sellable", year="2026", title="SELLABLE", fact="0 of 240 attacks moved money", img="work-sellable.jpg",
         desc="A shopping agent that structurally cannot spend your money. The model only proposes a product and a quantity; twelve plain rules decide. 578 tests.",
         links=["Code", "Architecture"]),
    dict(slug="abhed", year="2026", title="ABHED", fact="23 of 26 attacks blocked", img="work-abhed.jpg",
         desc="One gate for every action an AI agent takes. Risky actions wait for a person, and every decision lands on a signed, hash-chained ledger. Team of five, CodeX 3.0.",
         links=["Live app", "Code", "MCP server"]),
    dict(slug="proctoriq", year="2026", title="PROCTORIQ", fact="Video never leaves the device", img="work-proctoriq.jpg",
         desc="Exam-integrity analytics that run in the browser. A 27 KB model watches; the server only sees events, re-scores them and signs the report with HMAC-SHA256.",
         links=["Live site", "Code"]),
    dict(slug="fraud", year="2025", title="FRAUD DETECTION", fact="PR-AUC 0.793 on unseen time", img="work-fraud.jpg",
         desc="I rebuilt a 99.75%-accuracy notebook into an evaluation that would survive deployment, and kept the finding that hurt: it barely beats logistic regression.",
         links=["Live API", "Code"]),
    dict(slug="chokepoints", year="2026", title="CHOKE POINTS", fact="3,400 reasoning traces", img="work-research.jpg",
         desc="Where does an LLM's chain of thought first go wrong, and can you see failure coming? A six-author study; I built the pipeline. Modest results, reported as modest.",
         links=["Code"]),
]


def plate(p, i):
    W, H = 1280, 760
    PX, PW, PH, PY = 200, 880, 550, 34
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<clipPath id="pc"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}"/></clipPath>',
         f'<g clip-path="url(#pc)"><image href="{jpg(p["img"])}" x="{PX - 30}" y="{PY - 20}" width="{PW + 60}" height="{PH + 40}" preserveAspectRatio="xMidYMid slice">'
         f'<animateTransform attributeName="transform" type="translate" values="0 0;-24 -12;0 0" dur="16s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></image></g>']
    by, bh = PY + PH / 2 - 34, 68
    band = (f'<rect x="0" y="{by}" width="{W}" height="{bh}" fill="{BAND}"/>'
            + t(MED, p["year"], 21, 40, by + 42, MUT)
            + t(BOLD, p["title"], 34, 168, by + 46, INK, -0.02)
            + t(SEMI, p["fact"], 22, W - 40, by + 43, INK, 0, "end"))
    b.append(f'<g>{band}<animateTransform attributeName="transform" type="translate" values="-{W} 0;-{W} 0;0 0" keyTimes="0;0.13;1" calcMode="spline" keySplines="0 0 1 1;0.16 1 0.3 1" dur="1.15s" fill="freeze"/></g>')
    lw = sum(SEMI.width(l, 22) + 30 for l in p["links"])
    d, n = para(REG, p["desc"], 23, PX, PY + PH + 50, min(600, PW - lw - 30), 1.4)
    links = ""
    x = PX + PW
    for label in reversed(p["links"]):
        links += underline_link(SEMI, label, 22, x, PY + PH + 50, INK, "end")
        x -= SEMI.width(label, 22) + 30
    b.append(fade(d + links, 0.5))
    alt = f'{p["title"].title()}, {p["year"]}. {p["fact"]}. {p["desc"]}'
    return svg(W, H, "".join(b), alt)


# ---------------------------------------------------------------- proof marquee
def proof():
    W, H = 1280, 200
    items = ["Smart India Hackathon winner, college round", "Razorpay AI Buildathon", "CodeX 3.0 Hack Arena",
             "Decode Labs ML internship", "AWS Cloud Practitioner"]
    size, gap = 104, 60
    run, x = "", 0.0
    for it in items:
        run += t(BLACK, it, size, x, 140, BG, -0.04)
        x += BLACK.width(it, size, -0.04) + gap
        run += f'<circle cx="{x:.1f}" cy="104" r="9" fill="{BG}"/>'
        x += gap
    L = x
    body = (f'<rect width="{W}" height="{H}" fill="{INK}"/>'
            f'<g><g>{run}</g><g transform="translate({L:.1f} 0)">{run}</g>'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-{L:.1f} 0" dur="{L / 90:.0f}s" repeatCount="indefinite"/></g>')
    return svg(W, H, body, "Where the work has been tested: " + "; ".join(items) + ".")


# ---------------------------------------------------------------- about
def about():
    W, H = 1280, 720
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    st = ("I'm a third-year student who builds the part of an AI system that says no. "
          "My agents propose; plain, testable rules decide what actually happens.")
    d, n = para(MED, st, 40, 40, 110, 1040, 1.25)
    b.append(fade(d, 0.1))
    d2, _ = para(REG, "I evaluate models the way they'd be deployed, and I publish the caveat next to the number. "
                      "If a result is modest, the page says modest.", 24, 40, 110 + n * 50 + 40, 760, 1.4, MUT)
    b.append(fade(d2, 0.3))
    y0 = 110 + n * 50 + 40 + 2 * 34 + 70
    facts = [("Studying", "B.Tech AI & ML, KIET"), ("Graduating", "2028"), ("Based in", "Delhi NCR, India")]
    f = ""
    for i, (k, v) in enumerate(facts):
        f += t(REG, k, 19, 40, y0 + i * 72, MUT) + t(SEMI, v, 22, 40, y0 + 28 + i * 72, INK)
    b.append(fade(f, 0.45))
    rows = [("Smart India Hackathon", "Winner, college round"), ("Razorpay AI Buildathon", "SELLABLE"),
            ("CodeX 3.0 Hack Arena", "Abhed, team of five"), ("Decode Labs", "ML internship"),
            ("AWS Cloud Practitioner", "Certified")]
    r = t(SEMI, "Built and won", 19, 560, y0, MUT)
    for i, (k, v) in enumerate(rows):
        yy = y0 + 44 + i * 40
        r += t(MED, k, 22, 560, yy, INK) + t(REG, v, 21, W - 40, yy, MUT, 0, "end")
    b.append(fade(r, 0.6))
    return svg(W, H, "".join(b), "About: " + st + " Studying B.Tech AI & ML at KIET, graduating 2028, based in Delhi NCR.")


# ---------------------------------------------------------------- tools
TOOLS = [("Python", "Every project"), ("TypeScript and React", "ProctorIQ, Abhed"), ("PyTorch and ONNX", "ProctorIQ"),
         ("XGBoost and scikit-learn", "Fraud detection"), ("FastAPI and SQLite", "SELLABLE, ProctorIQ"),
         ("Next.js and Supabase", "Abhed"), ("MCP servers", "SELLABLE, abhed-mcp"), ("Statistics", "Research")]


def tools():
    W, H = 1280, 720
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<rect x="40" y="40" width="512" height="640" fill="{SURF}"/>',
         f'<clipPath id="tc"><rect x="40" y="40" width="512" height="640"/></clipPath>']
    imgs = ["tool-python.jpg", "tool-torch.jpg", "tool-mcp.jpg", "tool-research.jpg"]
    n = len(imgs)
    g = ""
    for i, im in enumerate(imgs):
        vals = ";".join("1" if j == i else "0" for j in range(n)) + (";1" if i == 0 else ";0")
        g += (f'<image href="{jpg(im)}" x="40" y="40" width="512" height="640" preserveAspectRatio="xMidYMid slice" opacity="{1 if i == 0 else 0}">'
              f'<animate attributeName="opacity" values="{vals}" dur="{n * 3}s" calcMode="discrete" repeatCount="indefinite"/></image>')
    b.append(f'<g clip-path="url(#tc)">{g}</g>')
    b.append(fade(t(BLACK, "What I build with", 70, 640, 128, INK, -0.04), 0.1))
    rows = ""
    for i, (k, v) in enumerate(TOOLS):
        y = 214 + i * 62
        rows += t(SEMI, k, 30, 640, y, INK, -0.015) + t(REG, v, 19, W - 40, y - 4, MUT, 0, "end")
    b.append(fade(rows, 0.3))
    return svg(W, H, "".join(b), "What I build with: " + "; ".join(f"{k} ({v})" for k, v in TOOLS) + ".")


# ---------------------------------------------------------------- contact
def contact():
    W, H = 1280, 620
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>',
         t(SEMI, "Hiring for an ML, AI or full-stack", 30, 40, 70, BG, -0.01),
         t(SEMI, "internship? Write to me.", 30, 40, 110, BG, -0.01)]
    mail = rise(t(BLACK, "harshdubey98190@", 132, 34, 360, BG, -0.05), 160, 0.15)
    mail2 = rise(t(BLACK, "gmail.com", 132, 34, 494, BG, -0.05), 160, 0.3)
    b.append(f'<clipPath id="m1"><rect x="0" y="240" width="{W}" height="148"/></clipPath><g clip-path="url(#m1)">{mail}</g>')
    b.append(f'<clipPath id="m2"><rect x="0" y="388" width="{W}" height="140"/></clipPath><g clip-path="url(#m2)">{mail2}</g>')
    b.append(t(MED, "Delhi NCR  ·  open to 2026 internships", 21, 40, H - 40, BG))
    x = W - 40
    for label in reversed(["iamharshdubey.vercel.app", "LinkedIn", "GitHub"]):
        b.append(underline_link(SEMI, label, 21, x, H - 40, BG, "end"))
        x -= SEMI.width(label, 21) + 30
    return svg(W, H, "".join(b), "Hiring for an ML, AI or full-stack internship? Write to harshdubey98190@gmail.com.")


def foot():
    W, H = 1280, 120
    body = (f'<rect width="{W}" height="{H}" fill="{BAND}"/>'
            + t(REG, "Harsh Dubey, ML engineer", 20, 40, 70, MUT)
            + t(REG, "This page uses the same design as my portfolio. Pictures are from the projects themselves.", 20, W - 40, 70, MUT, 0, "end"))
    return svg(W, H, body, "Harsh Dubey, ML engineer.")


if __name__ == "__main__":
    save("hero.svg", hero())
    for i, p in enumerate(PROJECTS):
        save(f"work-{p['slug']}.svg", plate(p, i))
    save("proof.svg", proof())
    save("about.svg", about())
    save("tools.svg", tools())
    save("contact.svg", contact())
    save("foot.svg", foot())
