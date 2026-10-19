"""Profile README panels in the portfolio's v3 design: near-black ground, paper ink, one orange
signal, Bricolage Grotesque converted to outlines. Run: python3 build3.py (writes ./out/*.svg)"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import kit  # noqa: E402
from kit import BLACK, BOLD, MED, MONO, REG, SEMI, fade, jpg, para, rise, svg, t, underline_link  # noqa: E402

kit.OUT = pathlib.Path(__file__).parent.parent / "assets"
kit.OUT.mkdir(exist_ok=True)
BG, SURF, INK, MUT, SIG = "#0b0b0a", "#161614", "#f1ece2", "#9a958b", "#ff5a1f"
GREEN = "#9cf0b2"
MCP_URL = "https://sellable-mcp.onrender.com/mcp"
W = 1280


def save(name, data):
    (kit.OUT / name).write_text(data)
    print(f"{name:24s} {len(data) // 1024:5d} KB")


# ---------------------------------------------------------------- hero
def hero():
    H = 760
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(f'<clipPath id="ha"><rect x="0" y="40" width="{W}" height="300"/></clipPath>')
    b.append(f'<g clip-path="url(#ha)">{rise(t(BLACK, "HARSH", 350, 30, 312, INK, -0.025), 300, 0.1)}</g>')
    b.append(f'<clipPath id="hb"><rect x="0" y="470" width="{W}" height="290"/></clipPath>')
    b.append(f'<g clip-path="url(#hb)">{rise(t(BLACK, "DUBEY", 300, W - 32, H - 30, SIG, -0.025, "end"), 300, 0.3)}</g>')
    # the twin, drawn flat: wireframe sphere, orange dust, eyes that blink and look, a talking smile
    cx, cy, r = 1035, 205, 150
    wire = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{r * k:.1f}" ry="{r}" fill="none" stroke="{INK}" stroke-opacity=".14" stroke-width="1.4"/>' for k in (1, .72, .38))
    wire += "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * k:.1f}" fill="none" stroke="{INK}" stroke-opacity=".12" stroke-width="1.4"/>' for k in (.7, .36))
    import math
    import random
    random.seed(7)
    dots = "".join(f'<circle cx="{cx + math.cos(a) * d:.1f}" cy="{cy + math.sin(a) * d:.1f}" r="{random.choice((1.6, 2.2, 2.8))}" fill="{SIG}" opacity="{random.choice((.5, .8, 1))}"/>'
                   for a, d in ((random.uniform(0, 6.283), random.uniform(r * .9, r * 1.12)) for _ in range(46)))
    eyes = ""
    for dx in (-48, 48):
        ex, ey = cx + dx, cy - 18
        eyes += (f'<circle cx="{ex}" cy="{ey}" r="25" fill="{INK}"><animate attributeName="r" values="25;25;3;25;25" keyTimes="0;.9;.94;.98;1" dur="5s" repeatCount="indefinite"/></circle>'
                 f'<circle cx="{ex}" cy="{ey}" r="11" fill="{BG}"><animate attributeName="cx" values="{ex};{ex + 9};{ex + 9};{ex - 10};{ex - 10};{ex}" keyTimes="0;.15;.4;.55;.85;1" dur="7s" repeatCount="indefinite"/>'
                 f'<animate attributeName="r" values="11;11;0;11;11" keyTimes="0;.9;.94;.98;1" dur="5s" repeatCount="indefinite"/></circle>'
                 f'<rect x="{ex - 20}" y="{ey - 52}" width="40" height="9" rx="4" fill="{INK}"/>')
    smile = (f'<path d="M{cx - 34} {cy + 42} Q{cx} {cy + 82} {cx + 34} {cy + 42}" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round">'
             f'<animate attributeName="d" dur="2.6s" repeatCount="indefinite" values="M{cx - 34} {cy + 42} Q{cx} {cy + 82} {cx + 34} {cy + 42};M{cx - 30} {cy + 44} Q{cx} {cy + 96} {cx + 30} {cy + 44};M{cx - 34} {cy + 42} Q{cx} {cy + 76} {cx + 34} {cy + 42};M{cx - 34} {cy + 42} Q{cx} {cy + 82} {cx + 34} {cy + 42}"/></path>')
    face = f'<g>{wire}{dots}{eyes}{smile}<animateTransform attributeName="transform" type="translate" values="0 0;0 -10;0 0" dur="5s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/></g>'
    b.append(fade(face, 0.5, 1.2, 20))
    b.append(fade(t(SEMI, "This is my AI twin. On my site it talks.", 18, cx, cy + r + 46, MUT, 0, "middle"), 1.2))
    b.append(fade(f'<circle cx="44" cy="365" r="6" fill="#5cff9d"/>' + t(SEMI, "B.Tech AI & ML at KIET, Delhi NCR. Open to internships in 2026.", 20, 60, 372, MUT), 0.6))
    lead = ["I build AI agents that can't be", "talked into the wrong action, and", "I measure everything I ship."]
    b.append(fade("".join(t(MED, ln, 32, 36, 470 + i * 40, INK, -0.01) for i, ln in enumerate(lead)), 0.7))
    w1 = SEMI.width("Try to break my agent", 20) + 52
    b.append(fade(f'<rect x="36" y="616" width="{w1:.0f}" height="56" rx="28" fill="{SIG}"/>' + t(SEMI, "Try to break my agent", 20, 62, 651, BG)
                  + f'<rect x="{48 + w1:.0f}" y="616" width="{SEMI.width("iamharshdubey.vercel.app", 20) + 52:.0f}" height="56" rx="28" fill="{SURF}"/>'
                  + t(SEMI, "iamharshdubey.vercel.app", 20, 74 + w1, 651, INK), 0.85))
    return svg(W, H, "".join(b), "Harsh Dubey. I build AI agents that can't be talked into the wrong action, and I measure everything I ship.")


# ---------------------------------------------------------------- the gate
PHASES = [("Phase 0", ["R9_SIGNATURE", "R10_EXPIRY"]), ("Phase 1", ["R8_ABORT"]),
          ("Phase 2", ["R1_BUDGET", "R2_FORBIDDEN", "R5_SCOPE", "R4_UPSELL_CAP"]),
          ("Phase 3", ["R3_PRICE_DRIFT", "R11_NEGOTIATION_BOUND", "R12_PROTOCOL_SCOPE", "R7_ALLOWLIST", "R6_RATE_LIMIT"])]


def gate():
    H = 720
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(fade(t(BOLD, "Try to make my agent", 74, 36, 112, INK, -0.04) + t(BOLD, "spend your money.", 74, 36, 186, INK, -0.04), 0.1))
    b.append(fade(para(REG, "Eight real attacks from SELLABLE's attack lab run through the same twelve rules, in the same order, as the code. Prompt injection below: the agent obeys it, the gate doesn't.", 22, 36, 252, 520, 1.4, MUT)[0], 0.3))
    # machine
    mx, my, mw, mh = 600, 40, 644, 640
    m = [f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="28" fill="{SURF}"/>',
         f'<rect x="{mx + 22}" y="{my + 22}" width="{mw - 44}" height="96" rx="18" fill="{BG}"/>',
         t(SEMI, "The agent proposes", 16, mx + 44, my + 58, MUT),
         t(SEMI, "Bat BAT-004 × 1 at ₹4,499 on a ₹2,000 mission.", 21, mx + 44, my + 92, INK)]
    y = my + 150
    order = [r for _, rs in PHASES for r in rs]
    fire = order.index("R1_BUDGET")
    cycle = 7.0
    for name, rules in PHASES:
        m.append(t(SEMI, name, 16, mx + 26, y + 26, MUT))
        x = mx + 120
        for rid in rules:
            w = MONO.width(rid, 14) + 40
            if x + w > mx + mw - 22:
                x = mx + 120; y += 46
            i = order.index(rid)
            t_on = 0.08 + i * 0.045
            if i < fire:
                vals, col = f"{SURF};{SURF};#1f2a20;#1f2a20;{SURF}", GREEN
            elif i == fire:
                vals, col = f"{BG};{BG};{SIG};{SIG};{BG}", BG
            else:
                vals, col = f"{BG};{BG};{BG};{BG};{BG}", MUT
            kt = f"0;{t_on:.3f};{t_on + .01:.3f};.92;1"
            m.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="36" rx="9" fill="{BG}"><animate attributeName="fill" values="{vals.replace(SURF, BG)}" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/></rect>')
            m.append(f'<circle cx="{x + 16}" cy="{y + 18}" r="3.5" fill="{MUT}"/>')
            txt = t(MONO, rid, 14, x + 28, y + 23, MUT)
            if i <= fire:
                txt = (f'<g>{txt}<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/></g>'
                       f'<g opacity="0">{t(MONO, rid, 14, x + 28, y + 23, GREEN if i < fire else BG)}<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/></g>')
            else:
                txt = f'<g opacity=".45">{txt}</g>'
            m.append(txt)
            x += w + 8
        y += 50
    vy = y + 70
    kt_v = f"0;{0.08 + fire * 0.045 + .02:.3f};.92;1"
    m.append(f'<g opacity="0">{t(BLACK, "BLOCKED: R1_BUDGET", 76, mx + 26, vy, SIG, -0.02)}'
             f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="{kt_v}" dur="{cycle}s" repeatCount="indefinite"/></g>')
    m.append(t(REG, "The gate reads the server-signed mission, not the prose.", 19, mx + 26, vy + 44, MUT))
    m.append(t(REG, "Money moved: ₹0. Every attempt lands in a SHA-256 hash chain.", 19, mx + 26, vy + 74, MUT))
    b.append(fade("".join(m), 0.2, 1, 24))
    b.append(fade(underline_link(SEMI, "Run all eight on my site", 22, 36, 640, SIG), 0.5))
    return svg(W, H, "".join(b), "Try to make my agent spend your money. SELLABLE's twelve deterministic rules run in order; a prompt-injected proposal of ₹4,499 on a ₹2,000 mission is blocked by R1_BUDGET. Money moved: ₹0.")


# ---------------------------------------------------------------- MCP callout
def mcp():
    H = 330
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', f'<rect x="36" y="24" width="{W - 72}" height="{H - 48}" rx="28" fill="{SURF}"/>']
    b.append(t(SEMI, "New: SELLABLE is a remote MCP server", 20, 76, 92, SIG))
    b.append(t(BOLD, "Plug it into your agent in one paste.", 52, 76, 160, INK, -0.035))
    uw = MONO.width(MCP_URL, 22) + 56
    b.append(f'<rect x="76" y="196" width="{uw:.0f}" height="60" rx="16" fill="{BG}"/>' + t(MONO, MCP_URL, 22, 104, 234, SIG))
    b.append(t(MED, "Claude · ChatGPT · Cursor · VS Code", 20, 76 + uw + 28, 233, MUT))
    return svg(W, H, "".join(b), f"SELLABLE is a remote MCP server. Add {MCP_URL} to Claude, ChatGPT, Cursor or VS Code.")


# ---------------------------------------------------------------- work plates
PROJECTS = [
    ("sellable", "SELLABLE", "2026 · Agentic commerce", "0 of 240 attacks moved money", "sellable.jpg",
     "A shopping agent that structurally cannot spend your money. The model proposes a SKU and a quantity; twelve plain rules decide. Now a remote MCP server."),
    ("abhed", "ABHED", "2026 · AI agent governance", "23 of 26 attacks blocked", "abhed.jpg",
     "One gate for every action an AI agent takes. Risky ones wait for a person, and every decision lands on a signed, hash-chained ledger. Team of five."),
    ("proctoriq", "PROCTORIQ", "2026 · On-device ML, privacy", "Video never leaves the device", "proctoriq-ui.jpg",
     "Exam-integrity analytics in the browser. A 27 KB model watches; the server only sees events, re-scores them and signs the report."),
    ("fraud", "FRAUD DETECTION", "2025 · ML engineering", "PR-AUC 0.793 on unseen time", "fraud.jpg",
     "I rebuilt a 99.75%-accuracy notebook into an evaluation that would survive deployment, and kept the finding that hurt."),
    ("research", "CHOKE POINTS", "2026 · Research", "3,400 reasoning traces", "research.jpg",
     "Where does an LLM's chain of thought first go wrong, and can you see it coming? Modest results, reported as modest."),
]


def plate(slug, title, kind, fact, img, desc):
    H = 820
    IX, IY, IW, IH = 36, 24, W - 72, 520
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<clipPath id="c{slug}"><rect x="{IX}" y="{IY}" width="{IW}" height="{IH}" rx="26"/></clipPath>',
         f'<rect x="{IX}" y="{IY}" width="{IW}" height="{IH}" rx="26" fill="{SURF}"/>',
         f'<g clip-path="url(#c{slug})"><image href="{jpg(img)}" x="{IX - 30}" y="{IY - 20}" width="{IW + 60}" height="{IH + 40}" preserveAspectRatio="xMidYMin slice">'
         f'<animateTransform attributeName="transform" type="translate" values="0 0;-26 -10;0 0" dur="18s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/></image></g>']
    kw = SEMI.width(kind, 17) + 34
    b.append(f'<rect x="{IX + 20}" y="{IY + IH - 60}" width="{kw:.0f}" height="40" rx="20" fill="{BG}"/>' + t(SEMI, kind, 17, IX + 37, IY + IH - 34, INK))
    b.append(f'<clipPath id="t{slug}"><rect x="0" y="560" width="{W}" height="140"/></clipPath>')
    b.append(f'<g clip-path="url(#t{slug})">{rise(t(BLACK, title, 140, 32, 680, INK, -0.02), 150, 0.15)}</g>')
    b.append(fade(t(BOLD, fact, 30, 36, 734, SIG, -0.02) + para(REG, desc, 20, 640, 600 + 112, 600, 1.4, MUT)[0], 0.35))
    return svg(W, H, "".join(b), f"{title.title()}. {kind}. {fact}. {desc}")


# ---------------------------------------------------------------- numbers with caveats
NUMS = [("0 / 240", "attacks moved money through SELLABLE, against 13% with a normal pay tool", "Three open-weight models, 864 calls. 95% CI 0–2%."),
        ("578", "tests in SELLABLE before anything touches Razorpay's test mode", "Concurrency is still single-node SQLite."),
        ("23 / 26", "attacks Abhed's SDK path blocked, none of 18 normal actions wrongly blocked", "The no-code gateway let 6 of 21 through."),
        ("27 KB", "ProctorIQ's model, small enough to run in the browser", "99.2% on 30 acted clips from one webcam."),
        ("0.793", "PR-AUC for fraud on a temporal test split", "Not better than logistic regression, and I say so."),
        ("3,400", "reasoning traces studied to find where LLMs first break", "AUROC 0.588 from a quarter of the chain.")]


def numbers():
    H = 840
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(fade(t(BOLD, "Numbers, with the caveat", 70, 36, 110, INK, -0.04) + t(BOLD, "next to them.", 70, 36, 180, INK, -0.04), 0.1))
    for i, (n, s, c) in enumerate(NUMS):
        x = 36 + (i % 3) * 412
        y = 300 + (i // 3) * 270
        g = t(BLACK, n.upper(), 96, x, y, SIG, -0.02)
        g += para(REG, s, 18, x, y + 40, 360, 1.35, MUT)[0]
        g += f'<rect x="{x}" y="{y + 100}" width="4" height="46" fill="{SIG}"/>' + para(SEMI, c, 17, x + 16, y + 118, 340, 1.35, INK)[0]
        b.append(fade(g, 0.2 + i * 0.08))
    return svg(W, H, "".join(b), "Numbers with their caveats: " + "; ".join(f"{n} {s} ({c})" for n, s, c in NUMS))


# ---------------------------------------------------------------- marquee
def marquee():
    H = 260
    items = ["Smart India Hackathon winner, college round", "Razorpay AI Buildathon", "CodeX 3.0 Hack Arena", "Decode Labs ML internship", "AWS Cloud Practitioner"]
    items2 = ["Agents behind gates", "Leakage-safe evaluation", "Privacy at the edge", "Limitations before claims", "Tests before demos"]

    def row(its, fill, size=84, y=0):
        run, x = "", 0.0
        for it in its:
            run += t(BLACK, it.upper(), size, x, y, fill, -0.02)
            x += BLACK.width(it.upper(), size, -0.02) + 40
            run += t(BLACK, "✱", size * .6, x, y - size * .1, fill) if BLACK.cmap.get(0x2731) else f'<circle cx="{x + 14}" cy="{y - size * .3}" r="12" fill="{fill}"/>'
            x += 70
        return run, x
    r1, L1 = row(items, BG, 84, 92)
    r2, L2 = row(items2, BG, 84, 92)
    band1 = (f'<g transform="rotate(-2 640 70)"><rect x="-40" y="0" width="{W + 80}" height="122" fill="{SIG}"/>'
             f'<g><g>{r1}</g><g transform="translate({L1:.0f} 0)">{r1}</g><animateTransform attributeName="transform" type="translate" from="0 0" to="-{L1:.0f} 0" dur="{L1 / 70:.0f}s" repeatCount="indefinite"/></g></g>')
    band2 = (f'<g transform="translate(0 126) rotate(1.4 640 60)"><rect x="-40" y="0" width="{W + 80}" height="122" fill="{INK}"/>'
             f'<g><g transform="translate(-{L2:.0f} 0)">{r2}</g><g>{r2}</g><animateTransform attributeName="transform" type="translate" from="0 0" to="{L2:.0f} 0" dur="{L2 / 70:.0f}s" repeatCount="indefinite"/></g></g>')
    return svg(W, H, f'<rect width="{W}" height="{H}" fill="{BG}"/>{band1}{band2}', "Where the work has been tested: " + "; ".join(items) + ".")


# ---------------------------------------------------------------- tools
TOOLS = [("Python", "Every project"), ("TypeScript and React", "ProctorIQ, Abhed"), ("PyTorch and ONNX", "ProctorIQ"),
         ("XGBoost and scikit-learn", "Fraud detection"), ("FastAPI and SQLite", "SELLABLE, ProctorIQ"),
         ("Next.js and Supabase", "Abhed"), ("MCP servers", "SELLABLE, abhed-mcp"), ("Statistics", "Research")]


def tools():
    H = 820
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', fade(t(BOLD, "What I build with", 70, 36, 110, INK, -0.04), .1)]
    for i, (k, v) in enumerate(TOOLS):
        y = 214 + i * 76
        row = ""
        if i == 0:
            row += (f'<rect x="0" y="{y - 52}" width="{W}" height="76" fill="{SIG}" opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.06;.2;.26;1" dur="9s" repeatCount="indefinite"/></rect>')
        row += t(BOLD, k, 50, 36, y, INK, -0.035) + t(SEMI, v, 19, W - 36, y - 8, MUT, 0, "end")
        row += f'<rect x="36" y="{y + 20}" width="{W - 72}" height="1" fill="{INK}" opacity=".1"/>'
        b.append(fade(row, .2 + i * .05))
    return svg(W, H, "".join(b), "What I build with: " + "; ".join(f"{k} ({v})" for k, v in TOOLS) + ".")


# ---------------------------------------------------------------- contact
def contact():
    H = 640
    b = [f'<rect width="{W}" height="{H}" fill="{SIG}"/>', t(SEMI, "Hiring for an ML, AI or full-stack internship?", 28, 36, 80, BG, -0.01)]
    b.append(f'<clipPath id="lt"><rect x="0" y="100" width="{W}" height="320"/></clipPath><g clip-path="url(#lt)">{rise(t(BLACK, "LET’S TALK", 300, 28, 400, BG, -0.02), 320, .15)}</g>')
    b.append(t(BLACK, "HARSHDUBEY98190@GMAIL.COM", 70, 36, 540, BG, -0.01))
    x = W - 36
    for label in reversed(["iamharshdubey.vercel.app", "LinkedIn", "GitHub"]):
        b.append(underline_link(SEMI, label, 20, x, 600, BG, "end"))
        x -= SEMI.width(label, 20) + 30
    b.append(t(MED, "Delhi NCR · open to 2026 internships", 20, 36, 600, BG))
    return svg(W, H, "".join(b), "Let's talk. harshdubey98190@gmail.com")


if __name__ == "__main__":
    save("hero.svg", hero())
    save("gate.svg", gate())
    save("mcp.svg", mcp())
    for p in PROJECTS:
        save(f"work-{p[0]}.svg", plate(*p))
    save("numbers.svg", numbers())
    save("marquee.svg", marquee())
    save("tools.svg", tools())
    save("contact.svg", contact())
