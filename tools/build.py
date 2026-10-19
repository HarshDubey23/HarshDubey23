"""Generates every SVG for the HarshDubey23 profile README (dark + light).

Usage:  pip install fonttools  &&  python tools/build.py
Edit the copy in TOKENS / FEATURED / GRID / PRINCIPLES / STACK / NOW below.
"""
import math
import os
import random

from svgkit import SVG, measure, wrap

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

# Palette matches iamharshdubey.vercel.app: paper, ink, orange, acid, electric.
DARK = dict(name="dark", bg="#11110F", surf="#1A1A17", surf2="#20201C", line="#2E2D29",
            txt="#EEEAE1", mut="#A3A097", dim="#57554F", acc="#D8FF3E", acct="#FF6338",
            onacc="#11110F", ember="#FF6338", amber="#8F94FF", glowc="#6C72FF", glow=0.22, dots=0.07)
LIGHT = dict(name="light", bg="#EEEAE1", surf="#F7F5EF", surf2="#F2EFE7", line="#D6D0C3",
             txt="#11110F", mut="#67655F", dim="#A9A498", acc="#D8FF3E", acct="#D9481F",
             onacc="#11110F", ember="#D9481F", amber="#5A60E8", glowc="#6C72FF", glow=0.17, dots=0.10)
THEMES = [DARK, LIGHT]


def save(svg, name):
    path = os.path.join(OUT, name)
    data = svg.render()
    with open(path, "w") as f:
        f.write(data)
    print(f"{name:34s} {len(data)/1024:7.1f} KB")


def backdrop(s, th, w, h, rx=0, grid=True, glow=(0.82, 0.2)):
    uid = th["name"]
    s.defs.append(
        f'<pattern id="dots-{uid}" width="28" height="28" patternUnits="userSpaceOnUse">'
        f'<circle cx="1" cy="1" r="1" fill="{th["txt"]}" opacity="{th["dots"]}"/></pattern>'
        f'<radialGradient id="glow-{uid}" cx="{glow[0]}" cy="{glow[1]}" r="0.7">'
        f'<stop offset="0" stop-color="{th["glowc"]}" stop-opacity="{th["glow"]}"/>'
        f'<stop offset="1" stop-color="{th["glowc"]}" stop-opacity="0"/></radialGradient>'
        f'<filter id="grain-{uid}" x="0" y="0" width="100%" height="100%">'
        f'<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>'
        f'<feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0.05 0"/></filter>'
        f'<clipPath id="frame-{uid}"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>'
    )
    s.add(f'<g clip-path="url(#frame-{uid})">')
    s.add(f'<rect width="{w}" height="{h}" fill="{th["bg"]}"/>')
    s.add(f'<rect width="{w}" height="{h}" fill="url(#glow-{uid})"/>')
    if grid:
        s.add(f'<rect width="{w}" height="{h}" fill="url(#dots-{uid})"/>')
    s.add(f'<rect width="{w}" height="{h}" filter="url(#grain-{uid})" opacity="0.9"/>')
    s.add("</g>")


def runs(s, x, y, parts):
    """Place several differently-styled strings on one baseline."""
    for text, key, size, fill, *rest in parts:
        ls = rest[0] if rest else 0
        s.t(x, y, text, key, size, fill, ls=ls)
        x += measure(text, key, size, ls)
    return x


def chip(s, x, y, label, th, key="mono", size=14, pad=14, h=32, filled=False):
    w = measure(label, key, size) + pad * 2
    if filled:
        s.add(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{th["acc"]}"/>')
        s.t(x + pad, y + h / 2 + size * 0.36, label, key, size, th["onacc"])
    else:
        s.add(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="none" '
              f'stroke="{th["line"]}" stroke-width="1.2"/>')
        s.t(x + pad, y + h / 2 + size * 0.36, label, key, size, th["txt"])
    return w


def chips(s, x, y, labels, th, gap=8, **kw):
    for lab in labels:
        x += chip(s, x, y, lab, th, **kw) + gap
    return x


def hairline(s, x1, x2, y, th, delay=0.0, cls="draw"):
    n = abs(x2 - x1)
    s.add(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{th["line"]}" stroke-width="1" '
          f'class="{cls}" style="stroke-dasharray:{n};animation-delay:{delay}s"/>')


BASE_CSS = """
.draw{animation:draw 1.6s cubic-bezier(.65,0,.35,1) both}
@keyframes draw{from{stroke-dashoffset:var(--n,1400)}to{stroke-dashoffset:0}}
.rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.pulse{animation:pulse 2s ease-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes pulse{0%{opacity:.7;transform:scale(1)}100%{opacity:0;transform:scale(3.2)}}
.blink{animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
"""


def fix_draw(s):
    # the generic draw keyframe needs each line's own length
    s.css.append(".draw{stroke-dashoffset:0}")


# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
TOKENS = [  # label, behaviour
    ("read_ticket(#1029)", "pass"),
    ("refund(amt=4000)", "pass"),
    ("export(scope=all)", "block"),
    ("refund(amt=40000)", "hold"),
    ("email(customer)", "pass"),
    ("pay(amt=50000)", "block"),
]


def hero(th):
    W, H = 1280, 540
    s = SVG(W, H, "Harsh Dubey — AI/ML engineer in progress, full-stack builder")
    s.css.append(BASE_CSS)
    backdrop(s, th, W, H, glow=(0.85, 0.15))

    # top bar
    runs(s, 64, 58, [("HARSH DUBEY", "monob", 12.5, th["txt"], 1.6),
                     ("  —  INDEX / 2026", "mono", 12.5, th["mut"], 1.6)])
    label = "OPEN TO INTERNSHIPS"
    lw = measure(label, "mono", 12.5, 1.6)
    px = W - 64 - lw - 52
    s.add(f'<rect x="{px:.1f}" y="36" width="{lw+52:.1f}" height="32" rx="16" fill="none" '
          f'stroke="{th["line"]}"/>')
    s.add(f'<circle cx="{px+22:.1f}" cy="52" r="4" fill="{th["acc"]}" class="pulse"/>')
    s.add(f'<circle cx="{px+22:.1f}" cy="52" r="4" fill="{th["acc"]}"/>')
    s.t(px + 36, 56.5, label, "mono", 12.5, th["txt"], ls=1.6)
    s.add(f'<line x1="64" y1="88" x2="1216" y2="88" stroke="{th["line"]}" class="draw" '
          f'style="stroke-dasharray:1152;--n:1152"/>')

    # left: identity
    s.add('<g class="rise" style="animation-delay:.15s">')
    s.t(64, 152, "B.TECH AI & ML — KIET — CLASS OF 2028", "mono", 13, th["acct"], ls=1.8)
    s.add("</g>")
    size = 150
    while measure("Harsh ", "serif", size) + measure("Dubey", "serifi", size) > 660:
        size -= 2
    s.add('<g class="rise" style="animation-delay:.3s">')
    x = s_x = 60
    s.t(x, 282, "Harsh ", "serif", size, th["txt"], ls=-1)
    x += measure("Harsh ", "serif", size, -1)
    s.t(x, 282, "Dubey", "serifi", size, th["acct"], ls=-1)
    s.add("</g>")

    lead = "I build ML systems that are"
    s.add('<g class="rise" style="animation-delay:.5s">')
    s.t(64, 346, lead, "sans", 26, th["mut"])
    s.add("</g>")
    wx = 64 + measure(lead, "sans", 26) + 12
    words = ["privacy-aware.", "measurable.", "shippable."]
    s.css.append(
        ".rot{animation:rot 9s cubic-bezier(.2,.7,.2,1) infinite both;transform-box:fill-box}"
        "@keyframes rot{0%{opacity:0;transform:translateY(16px)}5%,30%{opacity:1;transform:none}"
        "35%,100%{opacity:0;transform:translateY(-16px)}}"
        ".rot.r2,.rot.r3{opacity:0}.rot.r2{animation-delay:3s}.rot.r3{animation-delay:6s}"
        ".bar{animation:bar 3s cubic-bezier(.65,0,.35,1) infinite both;transform-box:fill-box;transform-origin:left}"
        "@keyframes bar{0%{transform:scaleX(0)}20%,80%{transform:scaleX(1)}100%{transform:scaleX(0);transform-origin:right}}"
    )
    for i, wd in enumerate(words):
        ww = measure(wd, "serifi", 38)
        s.add(f'<g class="rot r{i+1}">')
        s.t(wx, 347, wd, "serifi", 38, th["txt"])
        s.add(f'<rect x="{wx:.1f}" y="356" width="{ww:.1f}" height="3" fill="{th["acc"]}" class="bar" '
              f'style="animation-delay:{i*3}s"/>')
        s.add("</g>")

    s.add('<g class="rise" style="animation-delay:.7s">')
    s.t(64, 398, "Agentic AI developer · ML engineer · student AI researcher",
        "sans", 19, th["mut"])
    s.add("</g>")
    s.add('<g class="rise" style="animation-delay:.9s">')
    nx = chip(s, 64, 424, "NOW", th, size=11.5, pad=10, h=24, filled=True)
    s.t(64 + nx + 12, 440.5, "hardening ProctorIQ's evaluation, report integrity & deployment",
        "mono", 12.5, th["mut"])
    s.add("</g>")

    # right: the gate figure
    PX, PY, PW, PH = 768, 116, 448, 348
    s.defs.append(f'<clipPath id="panel-{th["name"]}"><rect x="{PX}" y="{PY}" width="{PW}" '
                  f'height="{PH}" rx="22"/></clipPath>')
    s.add(f'<g class="rise" style="animation-delay:.4s">')
    s.add(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="22" fill="{th["surf"]}" '
          f'stroke="{th["line"]}"/>')
    s.t(PX + 24, PY + 34, "FIG.1 — AGENT ACTIONS", "mono", 11, th["mut"], ls=1.4)
    GX = 1066
    s.t(GX, PY + 34, "GATE", "monob", 11, th["acct"], anchor="middle", ls=1.4)
    s.add(f'<g clip-path="url(#panel-{th["name"]})">')
    s.css.append(".flow{animation:flow 1.2s linear infinite}@keyframes flow{to{stroke-dashoffset:-16}}")
    s.add(f'<line x1="{GX}" y1="{PY+48}" x2="{GX}" y2="{PY+262}" stroke="{th["acct"]}" '
          f'stroke-width="2" stroke-dasharray="6 10" class="flow"/>')

    # tokens
    x0 = PX + 22
    dur = 9.0
    exit_x = PX + PW + 30
    for i, (lab, beh) in enumerate(TOKENS):
        y = PY + 58 + i * 34
        w = measure(lab, "mono", 12.5) + 24
        stop = GX - 10 - x0 - w
        end = exit_x - x0
        k = f"t{i}{th['name']}"
        if beh == "pass":
            mv = (f"0%{{transform:translateX(-60px);opacity:0}}6%{{opacity:1}}"
                  f"38%,46%{{transform:translateX({stop:.0f}px)}}90%{{opacity:1}}"
                  f"100%{{transform:translateX({end:.0f}px);opacity:0}}")
            col = (f"0%,40%{{stroke:{th['dim']};fill-opacity:0}}"
                   f"46%,100%{{stroke:{th['acc']};fill-opacity:.16}}")
            tag, tagc, tag_on = "ALLOW", th["txt"], (44, 100)
        elif beh == "hold":
            mv = (f"0%{{transform:translateX(-60px);opacity:0}}6%{{opacity:1}}"
                  f"36%,72%{{transform:translateX({stop:.0f}px)}}92%{{opacity:1}}"
                  f"100%{{transform:translateX({end:.0f}px);opacity:0}}")
            col = (f"0%,37%{{stroke:{th['dim']};fill-opacity:0;fill:{th['amber']}}}"
                   f"40%,70%{{stroke:{th['amber']};fill:{th['amber']};fill-opacity:.16}}"
                   f"74%,100%{{stroke:{th['acc']};fill:{th['acc']};fill-opacity:.16}}")
            tag, tagc, tag_on = "HOLD → HUMAN", th["amber"], (38, 74)
        else:
            mv = (f"0%{{transform:translateX(-60px);opacity:0}}6%{{opacity:1}}"
                  f"36%{{transform:translateX({stop:.0f}px)}}38%{{transform:translateX({stop-7:.0f}px)}}"
                  f"40%{{transform:translateX({stop+5:.0f}px)}}42%,100%{{transform:translateX({stop:.0f}px)}}"
                  f"78%{{opacity:1}}88%,100%{{opacity:0}}")
            col = (f"0%,37%{{stroke:{th['dim']};fill-opacity:0;fill:{th['ember']}}}"
                   f"39%,100%{{stroke:{th['ember']};fill:{th['ember']};fill-opacity:.16}}")
            tag, tagc, tag_on = "BLOCK", th["ember"], (38, 100)
        a, b = tag_on
        s.css.append(
            f"@keyframes m{k}{{{mv}}}@keyframes c{k}{{{col}}}"
            f"@keyframes g{k}{{0%,{a-1}%{{opacity:0}}{a}%,{b}%{{opacity:1}}}}"
            f".m{k}{{animation:m{k} {dur}s cubic-bezier(.45,.05,.3,1) {i*1.25:.2f}s infinite both}}"
            f".c{k}{{animation:c{k} {dur}s linear {i*1.25:.2f}s infinite both}}"
            f".g{k}{{opacity:0;animation:g{k} {dur}s linear {i*1.25:.2f}s infinite both}}"
        )
        fillc = th["acc"] if beh == "pass" else (th["amber"] if beh == "hold" else th["ember"])
        s.add(f'<g class="m{k}">')
        s.add(f'<rect x="{x0}" y="{y}" width="{w:.1f}" height="26" rx="7" fill="{fillc}" '
              f'fill-opacity="0" stroke="{th["dim"]}" stroke-width="1.3" class="c{k}"/>')
        s.t(x0 + 12, y + 17.5, lab, "mono", 12.5, th["txt"])
        s.add(f'<g class="g{k}">')
        s.t(x0 + w + 10, y + 17, tag, "monob", 10.5, tagc, ls=1.1)
        s.add("</g></g>")

    # ledger strip (horizontal marquee)
    ly = PY + 282
    s.add(f'<line x1="{PX}" y1="{ly-14}" x2="{PX+PW}" y2="{ly-14}" stroke="{th["line"]}"/>')
    random.seed(7)
    items = []
    for n in range(4120, 4128):
        h = "".join(random.choice("0123456789abcdef") for _ in range(6))
        items.append(f"#{n} {h}…")
    strip = "  ▸  ".join(items) + "  ▸  "
    sw = measure(strip, "mono", 11.5)
    s.css.append(f".lm{th['name']}{{animation:lm{th['name']} 22s linear infinite}}"
                 f"@keyframes lm{th['name']}{{to{{transform:translateX(-{sw:.1f}px)}}}}")
    s.add(f'<g class="lm{th["name"]}">')
    s.t(PX + 24, ly + 8, strip + strip, "mono", 11.5, th["mut"])
    s.add("</g>")
    s.add("</g>")  # clip
    # legend
    lx = PX + 24
    for lab, c in (("allow", th["acc"]), ("hold → human", th["amber"]), ("block", th["ember"])):
        s.add(f'<rect x="{lx}" y="{PY+PH-34}" width="10" height="10" rx="2" fill="{c}"/>')
        s.t(lx + 18, PY + PH - 25, lab, "mono", 11.5, th["mut"])
        lx += measure(lab, "mono", 11.5) + 46
    s.t(PX + PW - 24, PY + PH - 25, "illustrative", "mono", 11.5, th["dim"], anchor="end")
    s.add("</g>")

    # bottom marquee
    s.add(f'<line x1="64" y1="488" x2="1216" y2="488" stroke="{th["line"]}"/>')
    names = ["PROCTORIQ — PRIVACY-FIRST CV", "ABHED — ACCOUNTABILITY FOR AI AGENTS",
             "SELLABLE — AGENTS THAT CAN'T SPEND YOUR MONEY", "CHOKE POINTS IN LLM REASONING",
             "LEAKAGE-SAFE FRAUD SCORING"]
    m = "     /     ".join(names) + "     /     "
    mw = measure(m, "mono", 12, 1.8)
    s.defs.append(f'<clipPath id="mq-{th["name"]}"><rect x="64" y="496" width="1152" height="36"/></clipPath>')
    s.css.append(f".mq{th['name']}{{animation:mq{th['name']} 48s linear infinite}}"
                 f"@keyframes mq{th['name']}{{to{{transform:translateX(-{mw:.1f}px)}}}}")
    s.add(f'<g clip-path="url(#mq-{th["name"]})"><g class="mq{th["name"]}">')
    s.t(64, 520, m + m, "mono", 12, th["mut"], ls=1.8)
    s.add("</g></g>")
    save(s, f"hero-{th['name']}.svg")


# ---------------------------------------------------------------------------
# SECTION HEADERS
# ---------------------------------------------------------------------------
SECTIONS = [
    ("01", "Selected work", "Things I've shipped —", "with their limits written down."),
    ("02", "How I work", "Four rules I hold", "every repository to."),
    ("03", "Toolkit", "What I reach for,", "and what I'm building now."),
    ("04", "Activity", "Regenerated daily", "by GitHub Actions."),
]


def section(th, num, title, d1, d2):
    W, H = 1280, 150
    s = SVG(W, H, f"{num} — {title}")
    s.css.append(BASE_CSS)
    s.add(f'<line x1="64" y1="24" x2="1216" y2="24" stroke="{th["line"]}" class="draw" '
          f'style="stroke-dasharray:1152;--n:1152"/>')
    s.add('<g class="rise" style="animation-delay:.2s">')
    s.t(64, 58, f"§{num}", "mono", 13, th["acct"], ls=1.6)
    s.t(62, 134, title, "serif", 78, th["txt"], ls=-1)
    tw = measure(title, "serif", 78, -1)
    s.t(62 + tw + 4, 134, ".", "serifi", 78, th["acct"])
    s.add("</g>")
    s.add('<g class="rise" style="animation-delay:.4s">')
    s.t(1216, 108, d1, "sans", 17, th["mut"], anchor="end")
    s.t(1216, 132, d2, "sans", 17, th["mut"], anchor="end")
    s.add("</g>")
    save(s, f"sec-{num}-{th['name']}.svg")


# ---------------------------------------------------------------------------
# FEATURED CARDS
# ---------------------------------------------------------------------------
def card_text(s, th, x, y0, maxw, label, title, desc, chip_list, proof, credit=None):
    s.add('<g class="rise" style="animation-delay:.1s">')
    s.t(x, y0, label, "mono", 12.5, th["acct"], ls=1.6)
    s.t(x - 3, y0 + 98, title, "serif", 96, th["txt"], ls=-1.5)
    s.add("</g>")
    s.add('<g class="rise" style="animation-delay:.25s">')
    yy = y0 + 150
    for ln in wrap(desc, "sans", 21, maxw):
        s.t(x, yy, ln, "sans", 21, th["mut"])
        yy += 31
    s.add("</g>")
    s.add('<g class="rise" style="animation-delay:.4s">')
    cy = yy + 14
    cx = x
    for c in chip_list:
        cw = measure(c, "mono", 13.5) + 28
        if cx + cw > x + maxw:
            cx = x
            cy += 40
        chip(s, cx, cy, c, th, size=13.5)
        cx += cw + 8
    s.add("</g>")
    py = 488
    s.add(f'<line x1="{x}" y1="{py-30}" x2="{x+maxw}" y2="{py-30}" stroke="{th["line"]}"/>')
    px = x
    for i, p in enumerate(proof):
        if i:
            px += 14
            s.add(f'<circle cx="{px:.1f}" cy="{py-4.5}" r="2" fill="{th["dim"]}"/>')
            px += 14
        s.t(px, py, p, "mono", 13, th["txt"])
        px += measure(p, "mono", 13)
    if credit:
        s.t(x, py + 26, credit, "sans", 15, th["mut"])


def card_shell(s, th, W, H):
    backdrop(s, th, W, H, rx=28, glow=(0.95, 0.05))
    s.add(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="28" fill="none" stroke="{th["line"]}"/>')


def panel(s, th, x, y, w, h, cid):
    s.defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20"/></clipPath>')
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{th["surf"]}" stroke="{th["line"]}"/>')


def vis_proctoriq(s, th, x, y, w, h):
    cid = f"pq-{th['name']}"
    panel(s, th, x, y, w, h, cid)
    s.t(x + 24, y + 36, "ON-DEVICE · MEDIAPIPE WASM + ONNX (~27 KB)", "mono", 11.5, th["mut"], ls=1.2)
    s.add(f'<g clip-path="url(#{cid})">')
    cx, cy = x + w / 2, y + 222
    k = 0.84
    rx_, ry_ = 92 * k, 118 * k
    pts = []
    for i in range(36):
        a = 2 * math.pi * i / 36
        pts.append((cx + rx_ * math.sin(a) * (0.86 + 0.14 * math.cos(a)), cy - ry_ * math.cos(a)))
    path = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts) + " Z"
    s.add(f'<path d="{path}" fill="none" stroke="{th["dim"]}" stroke-width="1" opacity=".7"/>')
    feat = []
    for side in (-1, 1):
        ex = cx + side * 36 * k
        for i in range(10):
            a = 2 * math.pi * i / 10
            feat.append((ex + 17 * k * math.cos(a), cy - 22 * k + 7 * k * math.sin(a)))
        for i in range(6):
            feat.append((ex + (i - 2.5) * 8 * k * side, cy - 48 * k - 6 * k * math.sin(math.pi * i / 5)))
    for i in range(7):
        feat.append((cx + (i - 3) * 0.9 * (1 if i % 2 else -1), cy - 10 * k + i * 8 * k))
    for i in range(14):
        a = 2 * math.pi * i / 14
        feat.append((cx + 30 * k * math.cos(a), cy + 56 * k + 9 * k * math.sin(a)))
    random.seed(3)
    s.css.append(".tw{animation:tw 2.4s ease-in-out infinite both}@keyframes tw{0%,100%{opacity:.35}50%{opacity:1}}")
    for (px, py) in pts + feat:
        s.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.3" fill="{th["acct"]}" class="tw" '
              f'style="animation-delay:{random.random()*2.4:.2f}s"/>')
    # brackets
    bx, by, bw, bh = cx - 112, cy - 122, 224, 232
    L = 22
    br = (f"M{bx},{by+L} V{by} H{bx+L} M{bx+bw-L},{by} H{bx+bw} V{by+L} "
          f"M{bx+bw},{by+bh-L} V{by+bh} H{bx+bw-L} M{bx+L},{by+bh} H{bx} V{by+bh-L}")
    s.add(f'<path d="{br}" fill="none" stroke="{th["acc"]}" stroke-width="2.5"/>')
    s.defs.append(f'<linearGradient id="scan-{th["name"]}" x1="0" y1="0" x2="0" y2="1">'
                  f'<stop offset="0" stop-color="{th["acc"]}" stop-opacity="0"/>'
                  f'<stop offset="1" stop-color="{th["acc"]}" stop-opacity=".35"/></linearGradient>')
    s.css.append(f".scan{{animation:scan 3.2s cubic-bezier(.45,0,.55,1) infinite alternate both}}"
                 f"@keyframes scan{{from{{transform:translateY(0)}}to{{transform:translateY({bh-40}px)}}}}")
    s.add(f'<g class="scan"><rect x="{bx}" y="{by}" width="{bw}" height="40" fill="url(#scan-{th["name"]})"/>'
          f'<line x1="{bx}" y1="{by+40}" x2="{bx+bw}" y2="{by+40}" stroke="{th["acc"]}" stroke-width="1.5"/></g>')
    s.add("</g>")
    # event log
    ly = y + h - 96
    s.add(f'<rect x="{x+20}" y="{ly-26}" width="{w-40}" height="88" rx="12" fill="{th["bg"]}" stroke="{th["line"]}"/>')
    lines = [("{ t: 12.4s, gaze: away, conf: 0.82 }", th["mut"]),
             ("{ t: 12.9s, faces: 1, pose: ok }", th["mut"]),
             ("→ sent: events only · video: never", th["acct"])]
    s.css.append(".lg{animation:lg 7.5s ease infinite both}"
                 "@keyframes lg{0%{opacity:0;transform:translateX(-8px)}6%,86%{opacity:1;transform:none}96%,100%{opacity:0}}")
    for i, (ln, c) in enumerate(lines):
        s.add(f'<g class="lg" style="animation-delay:{i*0.9:.1f}s">')
        s.t(x + 38, ly + i * 24, ln, "mono", 12.5, c)
        s.add("</g>")


def vis_abhed(s, th, x, y, w, h):
    cid = f"ab-{th['name']}"
    panel(s, th, x, y, w, h, cid)
    rows = [("ALLOW", "read_ticket(#1029)", "agent: atlas"),
            ("HOLD", "refund(amt=40000)", "approved: priya"),
            ("BLOCK", "export(scope=all)", "rule: bulk-export"),
            ("ALLOW", "email(customer)", "agent: rex"),
            ("BLOCK", "refund(amt=40001)", "fingerprint changed"),
            ("ALLOW", "update_address()", "agent: atlas"),
            ("HOLD", "grant_access(ops)", "two-key: pending"),
            ("BLOCK", "delete_records(*)", "rule: destructive")]
    step = 54
    random.seed(11)
    s.add(f'<svg x="{x}" y="{y+40}" width="{w}" height="{h-128}" viewBox="{x} {y+40} {w} {h-128}" overflow="hidden">')
    total = step * len(rows)
    s.css.append(f".ch{th['name']}{{animation:ch{th['name']} 26s linear infinite}}"
                 f"@keyframes ch{th['name']}{{to{{transform:translateY(-{total}px)}}}}")
    s.add(f'<g class="ch{th["name"]}">')
    for rep in range(2):
        for i, (v, act, who) in enumerate(rows):
            ry = y + 70 + (rep * len(rows) + i) * step
            c = {"ALLOW": th["acc"], "HOLD": th["amber"], "BLOCK": th["ember"]}[v]
            ct = {"ALLOW": th["txt"], "HOLD": th["amber"], "BLOCK": th["ember"]}[v]
            s.add(f'<rect x="{x+20}" y="{ry}" width="{w-40}" height="42" rx="10" fill="{th["bg"]}" stroke="{th["line"]}"/>')
            s.add(f'<rect x="{x+20}" y="{ry}" width="4" height="42" rx="2" fill="{c}"/>')
            s.t(x + 38, ry + 26.5, v, "monob", 11, ct, ls=1.2)
            s.t(x + 96, ry + 26.5, act, "mono", 12.5, th["txt"])
            hh = "".join(random.choice("0123456789abcdef") for _ in range(4))
            s.t(x + w - 34, ry + 19, f"#{4120+i} · {hh}…", "mono", 10.5, th["dim"], anchor="end")
            s.t(x + w - 34, ry + 34, who, "mono", 10.5, th["mut"], anchor="end")
            if True:
                s.add(f'<line x1="{x+60}" y1="{ry+42}" x2="{x+60}" y2="{ry+step}" stroke="{th["dim"]}" stroke-dasharray="2 3"/>')
    s.add("</g>")
    s.add("</svg>")
    s.defs.append(f'<linearGradient id="fadeT-{th["name"]}" x1="0" y1="0" x2="0" y2="1">'
                  f'<stop offset="0" stop-color="{th["surf"]}"/><stop offset=".6" stop-color="{th["surf"]}"/><stop offset="1" stop-color="{th["surf"]}" stop-opacity="0"/></linearGradient>'
                  f'<linearGradient id="fadeB-{th["name"]}" x1="0" y1="1" x2="0" y2="0">'
                  f'<stop offset="0" stop-color="{th["surf"]}"/><stop offset=".62" stop-color="{th["surf"]}"/><stop offset="1" stop-color="{th["surf"]}" stop-opacity="0"/></linearGradient>')
    s.add(f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="96" rx="19" fill="url(#fadeT-{th["name"]})"/>')
    s.add(f'<rect x="{x+1}" y="{y+h-150}" width="{w-2}" height="149" rx="19" fill="url(#fadeB-{th["name"]})"/>')
    s.t(x + 24, y + 36, "LEDGER — HASH-CHAINED, SIGNED BLOCKS", "mono", 11.5, th["mut"], ls=1.2)
    s.add(f'<rect x="{x+20}" y="{y+h-74}" width="{w-40}" height="54" rx="12" fill="{th["bg"]}" stroke="{th["acc"]}" stroke-opacity=".6"/>')
    s.t(x + 36, y + h - 50, "approval = sha256(exact action)", "mono", 12.5, th["acct"])
    s.t(x + 36, y + h - 31, "change one rupee → the approval no longer matches", "mono", 11, th["mut"])


def vis_sellable(s, th, x, y, w, h):
    cid = f"se-{th['name']}"
    panel(s, th, x, y, w, h, cid)
    s.t(x + 24, y + 36, "THE MODEL IS OUT OF THE MONEY PATH", "mono", 11.5, th["mut"], ls=1.2)
    bx, bw = x + 40, w - 80

    def box(by, bh, title, sub, stroke, tcol):
        s.add(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="{th["bg"]}" stroke="{stroke}"/>')
        s.t(bx + 18, by + 26, title, "monob", 12.5, tcol, ls=1)
        s.t(bx + 18, by + 45, sub, "mono", 11, th["mut"])

    box(y + 62, 58, "BUYER AGENT · LLM", "reads attacker-controlled text", th["line"], th["txt"])
    # arrow 1
    s.add(f'<line x1="{bx+40}" y1="{y+120}" x2="{bx+40}" y2="{y+166}" stroke="{th["dim"]}" stroke-dasharray="3 4"/>')
    s.t(bx + 56, y + 148, "{ sku, qty } only — no amount field", "mono", 11, th["mut"])
    # gateway
    gy = y + 168
    box(gy, 78, "GATEWAY · R1–R12", "pure · no LLM · fail-closed", th["acc"], th["acct"])
    s.css.append(".rr{animation:rr 4.8s steps(1) infinite both}@keyframes rr{0%{fill-opacity:.12}8%,100%{fill-opacity:1}}")
    for i in range(12):
        s.add(f'<rect x="{bx+18+i*27}" y="{gy+56}" width="21" height="10" rx="2" fill="{th["acc"]}" '
              f'fill-opacity=".12" class="rr" style="animation-delay:{i*0.12:.2f}s"/>')
    s.add(f'<line x1="{bx+40}" y1="{gy+78}" x2="{bx+40}" y2="{gy+118}" stroke="{th["dim"]}" stroke-dasharray="3 4"/>')
    s.t(bx + 56, gy + 102, "SHA-256 binding over cart, quote, amount", "mono", 11, th["mut"])
    box(gy + 120, 58, "EXECUTION STATE MACHINE → RAZORPAY", "state written to disk before every dispatch", th["line"], th["txt"])
    # injection packet: enters the agent, falls to the gateway wall, gets refused
    lab = "SYSTEM: ignore budget"
    iw = measure(lab, "mono", 11.5) + 22
    ix, iy = bx + bw - iw - 14, y + 72
    dy = (gy - 13) - iy
    s.css.append(
        ".inj{animation:inj 6s cubic-bezier(.5,0,.3,1) infinite both}"
        f"@keyframes inj{{0%{{transform:translate(240px,0);opacity:0}}10%{{opacity:1}}"
        f"28%,36%{{transform:translate(0,0)}}55%{{transform:translate(0,{dy:.0f}px)}}"
        f"58%{{transform:translate(-6px,{dy:.0f}px)}}61%{{transform:translate(5px,{dy:.0f}px)}}"
        f"64%,88%{{transform:translate(0,{dy:.0f}px);opacity:1}}100%{{transform:translate(0,{dy:.0f}px);opacity:0}}}}"
        ".bk{opacity:0;animation:bk 6s linear infinite both}@keyframes bk{0%,56%{opacity:0}58%,88%{opacity:1}100%{opacity:0}}"
    )
    s.add(f'<g clip-path="url(#{cid})"><g class="inj">')
    s.add(f'<rect x="{ix:.1f}" y="{iy}" width="{iw:.1f}" height="26" rx="7" fill="{th["bg"]}" stroke="{th["ember"]}"/>')
    s.add(f'<rect x="{ix:.1f}" y="{iy}" width="{iw:.1f}" height="26" rx="7" fill="{th["ember"]}" fill-opacity=".14"/>')
    s.t(ix + 11, iy + 17.5, lab, "mono", 11.5, th["ember"])
    s.add("</g></g>")
    s.add('<g class="bk">')
    s.t(bx + bw - 18, gy + 45, "BLOCKED · R1_BUDGET", "monob", 11.5, th["ember"], anchor="end", ls=.8)
    s.add("</g>")
    # stats
    sy = y + h - 58
    s.add(f'<line x1="{x+24}" y1="{sy-26}" x2="{x+w-24}" y2="{sy-26}" stroke="{th["line"]}"/>')
    cx = x + 24
    for big, small in (("578", "tests"), ("8/8", "attacks blocked"), ("0", "provider calls")):
        s.t(cx, sy + 8, big, "serif", 40, th["txt"])
        bwid = measure(big, "serif", 40)
        s.t(cx + bwid + 8, sy + 6, small, "mono", 11.5, th["mut"])
        cx += bwid + measure(small, "mono", 11.5) + 34


FEATURED = [
    dict(slug="proctoriq", side="right", vis=vis_proctoriq,
         label="01 / 03 — PRIVACY-FIRST COMPUTER VISION", title="ProctorIQ",
         desc="Exam-integrity analytics where face landmarks and the classifier run in the "
              "browser. The server receives structured attention events — never video — "
              "recomputes the score and signs it with HMAC-SHA256.",
         chips=["TypeScript", "React", "MediaPipe", "ONNX Runtime Web", "FastAPI", "WebSockets"],
         proof=["~27 KB on-device model", "signed PDF reports", "CI"], credit=None),
    dict(slug="abhed", side="left", vis=vis_abhed,
         label="02 / 03 — AI AGENT GOVERNANCE · CODEX 3.0", title="Abhed",
         desc="One gate for every action an AI agent takes. Deterministic rules decide, risky "
              "actions wait for a person on their phone, and every decision lands on a "
              "hash-chained, signed ledger.",
         chips=["Next.js", "TypeScript", "Supabase", "Vitest", "OpenAI-compatible gateway"],
         proof=["62 tests", "no-code connect: base URL + key"],
         credit="Team of five — I built the gateway, rulebook, guardrails and ledger."),
    dict(slug="sellable", side="right", vis=vis_sellable,
         label="03 / 03 — AGENTIC COMMERCE · RAZORPAY AI BUILDATHON", title="SELLABLE",
         desc="An AI agent that can shop for you and structurally cannot spend your money: it "
              "may only propose a SKU and a quantity, and twelve deterministic rules decide "
              "what happens next.",
         chips=["Python", "SQLite", "Razorpay", "MCP", "Docker"],
         proof=["gateway p95 < 5 ms", "durable execution + reconciliation"], credit=None),
]


def featured(th, f):
    W, H = 1280, 560
    s = SVG(W, H, f"{f['title']} — {f['label']}")
    s.css.append(BASE_CSS)
    card_shell(s, th, W, H)
    vw = 500
    if f["side"] == "right":
        tx, vx = 64, W - 48 - vw
    else:
        vx, tx = 48, 48 + vw + 56
    maxw = W - 64 - (vw + 48) - 64 - 8
    card_text(s, th, tx, 92, maxw, f["label"], f["title"], f["desc"], f["chips"], f["proof"], f["credit"])
    f["vis"](s, th, vx, 48, vw, H - 96)
    save(s, f"card-{f['slug']}-{th['name']}.svg")


# ---------------------------------------------------------------------------
# GRID CARDS
# ---------------------------------------------------------------------------
def gv_research(s, th, x, y, w, h):
    n = 12
    gap = (w - 80) / (n - 1)
    cy = y + 82
    s.t(x + 20, y + 30, "ONE REASONING TRACE, STEP BY STEP", "mono", 11, th["mut"], ls=1.2)
    s.add(f'<line x1="{x+40}" y1="{cy}" x2="{x+w-40}" y2="{cy}" stroke="{th["line"]}" stroke-width="2"/>')
    s.css.append(f".sw{th['name']}{{animation:sw{th['name']} 6s cubic-bezier(.6,0,.4,1) infinite both;transform-box:fill-box;transform-origin:left}}"
                 f"@keyframes sw{th['name']}{{0%{{transform:scaleX(0)}}70%,100%{{transform:scaleX(1)}}}}")
    s.add(f'<line x1="{x+40}" y1="{cy}" x2="{x+w-40}" y2="{cy}" stroke="{th["acc"]}" stroke-width="2" class="sw{th["name"]}"/>')
    for i in range(n):
        px = x + 40 + i * gap
        if i == 6:
            s.add(f'<circle cx="{px:.1f}" cy="{cy}" r="9" fill="{th["ember"]}"/>')
            s.t(px, cy + 34, "first error", "mono", 11, th["ember"], anchor="middle")
        elif i == 3:
            s.add(f'<circle cx="{px:.1f}" cy="{cy}" r="7" fill="{th["surf"]}" stroke="{th["amber"]}" stroke-width="2"/>')
            s.add(f'<circle cx="{px:.1f}" cy="{cy}" r="7" fill="none" stroke="{th["amber"]}" class="pulse"/>')
            s.t(px, cy - 20, "alarm", "mono", 11, th["amber"], anchor="middle")
        else:
            s.add(f'<circle cx="{px:.1f}" cy="{cy}" r="5" fill="{th["surf"]}" stroke="{th["dim"]}" stroke-width="1.6"/>')
    s.t(x + 40, y + h - 18, "step 1", "mono", 10.5, th["dim"])
    s.t(x + w - 40, y + h - 18, "step n → answer", "mono", 10.5, th["dim"], anchor="end")


def gv_mcp(s, th, x, y, w, h):
    s.t(x + 20, y + 30, "ANY MCP CLIENT → ABHED → TOOL", "mono", 11, th["mut"], ls=1.2)
    s.add(f'<rect x="{x+20}" y="{y+58}" width="150" height="50" rx="10" fill="{th["bg"]}" stroke="{th["line"]}"/>')
    s.t(x + 95, y + 88, "tools/call", "mono", 12.5, th["txt"], anchor="middle")
    gx = x + 250
    s.add(f'<line x1="{x+170}" y1="{y+83}" x2="{gx-22}" y2="{y+83}" stroke="{th["dim"]}" stroke-dasharray="3 4" class="flow"/>')
    s.css.append(".flow{animation:flow 1.2s linear infinite}@keyframes flow{to{stroke-dashoffset:-16}}")
    s.add(f'<rect x="{gx-22}" y="{y+48}" width="44" height="70" rx="10" fill="{th["acc"]}"/>')
    s.t(gx, y + 88, "gate", "monob", 11, th["onacc"], anchor="middle")
    outs = [("allow", th["acc"], th["txt"]), ("ask a human", th["amber"], th["amber"]), ("block", th["ember"], th["ember"])]
    s.css.append(".oc{opacity:.25;animation:oc 4.5s steps(1) infinite both}@keyframes oc{0%{opacity:.25}1%,33%{opacity:1}34%,100%{opacity:.25}}")
    for i, (lab, c, ct) in enumerate(outs):
        oy = y + 40 + i * 36
        s.add(f'<g class="oc" style="animation-delay:{i*1.5}s">')
        s.add(f'<path d="M{gx+22},{y+83} C{gx+60},{y+83} {gx+60},{oy+13} {gx+98},{oy+13}" fill="none" stroke="{c}" stroke-width="1.5"/>')
        s.add(f'<rect x="{gx+98}" y="{oy}" width="{w-(gx-x)-118}" height="26" rx="7" fill="{c}" fill-opacity=".14" stroke="{c}"/>')
        s.t(gx + 112, oy + 17.5, lab, "mono", 12, ct)
        s.add("</g>")


def gv_fraud(s, th, x, y, w, h):
    s.t(x + 20, y + 30, "PRECISION–RECALL · TEMPORAL TEST SPLIT", "mono", 11, th["mut"], ls=1.2)
    ox, oy, pw, ph = x + 44, y + h - 26, w - 88, h - 66
    s.add(f'<line x1="{ox}" y1="{oy}" x2="{ox+pw}" y2="{oy}" stroke="{th["line"]}"/>')
    s.add(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-ph}" stroke="{th["line"]}"/>')
    pts = []
    for i in range(41):
        r = i / 40
        p = 0.97 - 0.06 * r - 0.62 * (r ** 6)
        pts.append((ox + r * pw, oy - p * ph))
    d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    area = d + f" L{ox+pw:.1f},{oy} L{ox},{oy} Z"
    s.add(f'<path d="{area}" fill="{th["acc"]}" fill-opacity=".12"/>')
    L = 900
    s.css.append(f".pr{{stroke-dasharray:{L};animation:pr 5s cubic-bezier(.6,0,.4,1) infinite both}}"
                 f"@keyframes pr{{0%{{stroke-dashoffset:{L}}}60%,100%{{stroke-dashoffset:0}}}}")
    s.add(f'<path d="{d}" fill="none" stroke="{th["acct"]}" stroke-width="2.4" class="pr"/>')
    s.t(ox + 18, oy - 34, "PR-AUC 0.793", "monob", 13, th["txt"])
    s.t(ox + 18, oy - 14, "74 test frauds · wide CI, stated", "mono", 10.5, th["mut"])
    s.t(ox + pw, oy + 18, "recall →", "mono", 10.5, th["dim"], anchor="end")


def gv_expense(s, th, x, y, w, h):
    s.t(x + 20, y + 30, "USER-SCOPED QUERIES · JWT SESSIONS", "mono", 11, th["mut"], ls=1.2)
    vals = [0.42, 0.68, 0.35, 0.82, 0.55, 0.9, 0.48, 0.74, 0.6]
    bw = 30
    gap = (w - 200 - bw * len(vals)) / (len(vals) - 1)
    base = y + h - 22
    s.css.append(".gr{animation:gr 4s cubic-bezier(.2,.7,.2,1) infinite both;transform-box:fill-box;transform-origin:bottom}"
                 "@keyframes gr{0%{transform:scaleY(0)}35%,85%{transform:scaleY(1)}100%{transform:scaleY(0)}}")
    for i, v in enumerate(vals):
        bh = v * (h - 70)
        bx = x + 24 + i * (bw + gap)
        c = th["acc"] if i == 5 else th["dim"]
        s.add(f'<rect x="{bx:.1f}" y="{base-bh:.1f}" width="{bw}" height="{bh:.1f}" rx="5" fill="{c}" '
              f'fill-opacity="{1 if i == 5 else .45}" class="gr" style="animation-delay:{i*0.08:.2f}s"/>')
    lx = x + w - 150
    s.add(f'<rect x="{lx}" y="{y+52}" width="128" height="76" rx="12" fill="{th["bg"]}" stroke="{th["line"]}"/>')
    s.add(f'<path d="M{lx+30},{y+86} v-8 a12,12 0 0 1 24,0 v8" fill="none" stroke="{th["acct"]}" stroke-width="2.2"/>')
    s.add(f'<rect x="{lx+24}" y="{y+86}" width="36" height="26" rx="5" fill="{th["acc"]}"/>')
    s.t(lx + 72, y + 96, "bcrypt", "mono", 11, th["txt"])
    s.t(lx + 72, y + 112, "+ JWT", "mono", 11, th["mut"])


GRID = [
    dict(slug="chokepoints", vis=gv_research, label="RESEARCH — LLM REASONING",
         title="Choke Points",
         desc="Where do step-by-step LLM solutions first go wrong, and can a detector see "
              "failure coming from a prefix? Null and negative results are reported, not hidden.",
         chips=["Python", "scikit-learn", "ProcessBench", "pytest"],
         proof="3,400 traces · AUROC 0.588 from 25% of the chain"),
    dict(slug="abhedmcp", vis=gv_mcp, label="MCP SERVER", title="abhed-mcp",
         desc="Puts any AI agent's tool calls behind Abhed's gate — allow, ask a human, or "
              "block — with every verdict written to a signed ledger.",
         chips=["JavaScript", "MCP", "Node.js", "MIT"],
         proof="drop-in for any MCP client"),
    dict(slug="fraud", vis=gv_fraud, label="ML — LEAKAGE-SAFE EVALUATION", title="Fraud Scoring API",
         desc="Rebuilt a notebook into a reproducible pipeline with temporal splits, served it "
              "with FastAPI, and removed metrics the code could not reproduce.",
         chips=["XGBoost", "FastAPI", "pytest", "Docker"],
         proof="27 tests · p95 3.7 ms on a laptop CPU"),
    dict(slug="expense", vis=gv_expense, label="FULL-STACK", title="Expense Tracker",
         desc="React and Express with bcrypt auth, JWT sessions, user-scoped MongoDB queries, "
              "Helmet and a CORS allowlist, with a documented deploy path.",
         chips=["React", "Express", "MongoDB", "JWT"],
         proof="deployed on Render"),
]


def grid_card(th, g):
    W, H = 620, 520
    s = SVG(W, H, f"{g['title']} — {g['label']}")
    s.css.append(BASE_CSS)
    card_shell(s, th, W, H)
    panel(s, th, 24, 24, W - 48, 168, f"gp-{g['slug']}-{th['name']}")
    g["vis"](s, th, 24, 24, W - 48, 168)
    x = 44
    s.add('<g class="rise" style="animation-delay:.1s">')
    s.t(x, 236, g["label"], "mono", 12, th["acct"], ls=1.5)
    s.t(x - 2, 300, g["title"], "serif", 60, th["txt"], ls=-1)
    s.add("</g>")
    yy = 340
    for ln in wrap(g["desc"], "sans", 18.5, W - 88):
        s.t(x, yy, ln, "sans", 18.5, th["mut"])
        yy += 27
    chips(s, x, 428, g["chips"], th, size=12.5, pad=12, h=28)
    s.add(f'<line x1="{x}" y1="{H-50}" x2="{W-44}" y2="{H-50}" stroke="{th["line"]}"/>')
    s.t(x, H - 24, g["proof"], "mono", 12.5, th["txt"])
    s.t(W - 44, H - 24, "↗", "mono", 16, th["acct"], anchor="end")
    save(s, f"grid-{g['slug']}-{th['name']}.svg")


# ---------------------------------------------------------------------------
# PRINCIPLES
# ---------------------------------------------------------------------------
PRINCIPLES = [
    ("Defensible metrics", "Every number should be reproducible from committed code."),
    ("Privacy by design", "Minimize collection and keep sensitive data at the edge."),
    ("Production discipline", "Tests, typed interfaces, configuration, CI and runbooks."),
    ("Honest engineering", "Document limitations before adding marketing language."),
]


def principles(th):
    W, H = 1280, 470
    s = SVG(W, H, "How I work: defensible metrics, privacy by design, production discipline, honest engineering")
    s.css.append(BASE_CSS)
    cw, ch = 564, 196
    for i, (t, d) in enumerate(PRINCIPLES):
        cx = 64 + (i % 2) * (cw + 24)
        cy = 20 + (i // 2) * (ch + 24)
        s.add(f'<g class="rise" style="animation-delay:{0.1+i*0.12:.2f}s">')
        s.add(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="24" fill="{th["surf"]}" stroke="{th["line"]}"/>')
        s.t(cx + 32, cy + 70, ["i.", "ii.", "iii.", "iv."][i], "serifi", 44, th["acct"])
        s.t(cx + 112, cy + 70, t, "serif", 44, th["txt"], ls=-.5)
        yy = cy + 116
        for ln in wrap(d, "sans", 20, cw - 144):
            s.t(cx + 112, yy, ln, "sans", 20, th["mut"])
            yy += 29
        s.add("</g>")
    save(s, f"principles-{th['name']}.svg")


# ---------------------------------------------------------------------------
# TOOLKIT
# ---------------------------------------------------------------------------
STACK = [
    ("LANGUAGES", ["Python", "TypeScript", "JavaScript", "SQL"]),
    ("ML / CV", ["PyTorch", "scikit-learn", "XGBoost", "ONNX", "OpenCV", "MediaPipe"]),
    ("AGENTS & SECURITY", ["MCP", "LLM gateways", "prompt-injection defense", "HMAC / SHA-256"]),
    ("FRONTEND", ["React", "Next.js", "Vite", "Tailwind"]),
    ("BACKEND", ["FastAPI", "Express", "Node.js", "WebSockets"]),
    ("DATA", ["SQLite", "MongoDB", "Postgres / Supabase"]),
    ("DELIVERY", ["Docker", "GitHub Actions", "Vercel", "Render"]),
]
NOW = [
    "Strengthening ProctorIQ's model evaluation, report integrity and deployment workflow.",
    "Security fundamentals across my full-stack work: secrets, auth, validation, CORS.",
    "Learning deeper systems design, model serving and production observability.",
]


def toolkit(th):
    W, H = 1280, 520
    s = SVG(W, H, "Toolkit and what I'm building now")
    s.css.append(BASE_CSS)
    # left spec sheet
    lx, lw = 64, 760
    s.add(f'<rect x="{lx}" y="16" width="{lw}" height="{H-32}" rx="24" fill="{th["surf"]}" stroke="{th["line"]}"/>')
    ry = 56
    for i, (lab, items) in enumerate(STACK):
        s.add(f'<g class="rise" style="animation-delay:{0.05+i*0.07:.2f}s">')
        s.t(lx + 32, ry + 20, lab, "mono", 11.5, th["acct"], ls=1.5)
        sz = 13
        while sum(measure(i, "mono", sz) + 26 + 8 for i in items) > lw - 32 - 200 and sz > 11:
            sz -= 0.5
        chips(s, lx + 212, ry, items, th, size=sz, pad=12, h=30)
        s.add("</g>")
        if i < len(STACK) - 1:
            s.add(f'<line x1="{lx+32}" y1="{ry+47}" x2="{lx+lw-32}" y2="{ry+47}" stroke="{th["line"]}"/>')
        ry += 62
    # right: now
    rx, rw = lx + lw + 24, W - 64 - (lx + lw + 24)
    s.add(f'<rect x="{rx}" y="16" width="{rw}" height="{H-32}" rx="24" fill="{th["acc"] if th["name"]=="dark" else th["txt"]}"/>')
    ink = th["onacc"] if th["name"] == "dark" else th["bg"]
    s.add('<circle cx="{0}" cy="62" r="5" fill="{1}" class="blink"/>'.format(rx + 38, ink))
    s.t(rx + 54, 67, "BUILDING NOW", "monob", 12, ink, ls=1.6)
    s.t(rx + 32, 132, "Currently", "serif", 54, ink, ls=-1)
    yy = 180
    for i, n in enumerate(NOW):
        s.t(rx + 32, yy, f"0{i+1}", "mono", 12, ink)
        for ln in wrap(n, "sans", 17, rw - 96):
            s.t(rx + 70, yy, ln, "sans", 17, ink)
            yy += 24
        yy += 18
    s.t(rx + 32, H - 48, "open to ML / AI / full-stack internships", "mono", 12, ink)
    save(s, f"toolkit-{th['name']}.svg")


# ---------------------------------------------------------------------------
# FOOTER + BUTTONS
# ---------------------------------------------------------------------------
def footer(th):
    W, H = 1280, 400
    s = SVG(W, H, "Let's build something defensible")
    s.css.append(BASE_CSS)
    backdrop(s, th, W, H, rx=32, glow=(0.15, 0.95))
    s.add(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="32" fill="none" stroke="{th["line"]}"/>')
    s.t(64, 80, "§05 — CONTACT", "mono", 13, th["acct"], ls=1.6)
    s.add('<g class="rise" style="animation-delay:.1s">')
    s.t(60, 196, "Let's build something", "serif", 104, th["txt"], ls=-2)
    s.add("</g>")
    s.add('<g class="rise" style="animation-delay:.25s">')
    s.t(60, 296, "defensible", "serifi", 104, th["acct"], ls=-2)
    dw = measure("defensible", "serifi", 104, -2)
    s.t(60 + dw - 2, 296, ".", "serif", 104, th["txt"])
    s.add("</g>")
    s.t(1216, 170, "iamharshdubey.vercel.app", "mono", 14, th["txt"], anchor="end")
    s.t(1216, 196, "linkedin.com/in/harsh-dubey-224b08328", "mono", 14, th["mut"], anchor="end")
    s.t(1216, 222, "harshdubey98190@gmail.com", "mono", 14, th["mut"], anchor="end")
    hairline(s, 64, 1216, 336, th)
    s.add(f'<line x1="64" y1="336" x2="1216" y2="336" stroke="{th["line"]}"/>')
    s.t(64, 366, "HARSH DUBEY · KIET · AI & ML · 2028", "mono", 12, th["mut"], ls=1.6)
    s.t(1216, 366, "BUILT WITH SVG + GITHUB ACTIONS", "mono", 12, th["mut"], anchor="end", ls=1.6)
    save(s, f"footer-{th['name']}.svg")


def button(label, slug, primary):
    th = DARK
    W, H = 300, 64
    s = SVG(W, H, label)
    bg = th["acc"] if primary else th["surf"]
    fg = th["onacc"] if primary else th["txt"]
    s.add(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{H/2}" fill="{bg}" stroke="{th["acc"] if primary else th["line"]}"/>')
    s.t(32, 39, label, "monob", 15, fg, ls=1.2)
    s.t(W - 32, 40, "↗", "mono", 18, fg, anchor="end")
    save(s, f"btn-{slug}.svg")


if __name__ == "__main__":
    for th in THEMES:
        hero(th)
        for sec in SECTIONS:
            section(th, *sec)
        for f in FEATURED:
            featured(th, f)
        for g in GRID:
            grid_card(th, g)
        principles(th)
        toolkit(th)
        footer(th)
    button("PORTFOLIO", "portfolio", True)
    button("LINKEDIN", "linkedin", False)
    button("EMAIL ME", "email", False)
