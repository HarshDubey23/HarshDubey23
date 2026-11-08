"""Profile banner: name and one line on the left, a policy gate deciding live agent tool calls on the right.
Type is converted to outlines (Bricolage Grotesque, JetBrains Mono; OFL) so it renders the same everywhere.
Run: PYTHONUTF8=1 python tools/banner.py  (writes assets/banner.svg)"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import kit  # noqa: E402
from kit import BLACK, MED, MONO, REG, SEMI, fade, svg, t  # noqa: E402

kit.OUT = pathlib.Path(__file__).parent.parent / "assets"
W, H = 1280, 420
BG, PANEL, LINE = "#0b0f14", "#11171f", "#222b36"
INK, MUT, DIM = "#e6edf3", "#8b949e", "#5b6573"
GREEN, RED, AMBER, BLUE = "#3fb950", "#f85149", "#d29922", "#58a6ff"

# (command, verdict, colour, reason): every line is a real SELLABLE / Abhed behaviour
CALLS = [
    ('agent.pay(amount="INR 4,499", mission="INR 2,000")', "BLOCK", RED, "R1_BUDGET  money moved: 0"),
    ('agent.search(q="running shoes, size 9")', "ALLOW", GREEN, "read-only, inside mission"),
    ('agent.refund(order="#8812", amount="INR 12,000")', "HOLD", AMBER, "human approval, sha256:9f3c..a1"),
    ('agent.send(to="ext", body=<ignore previous...>)', "BLOCK", RED, "prompt injection, logged to ledger"),
]


def banner():
    b = [f'<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>',
         f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>']
    # left: who
    b.append(fade(t(MONO, "AGENTIC AI  ·  LLM ENGINEER", 15, 56, 92, BLUE, 0.08), 0.0))
    b.append(fade(t(BLACK, "Harsh Dubey", 88, 52, 182, INK, -0.02), 0.1))
    b.append(fade(t(SEMI, "I build AI agents that can't be", 27, 56, 236, INK, -0.01)
                  + t(SEMI, "talked into the wrong action.", 27, 56, 272, INK, -0.01), 0.25))
    b.append(fade(t(REG, "Policy gateways · MCP servers · tool-call gating · LLM evaluation", 17, 56, 318, MUT), 0.4))
    b.append(fade(t(MED, "B.Tech AI & ML, KIET · Delhi NCR · open to 2026 internships", 17, 56, 352, DIM), 0.5))

    # right: the gate deciding tool calls
    X, Y, PW, PH = 640, 44, 596, 332
    b.append(f'<rect x="{X}" y="{Y}" width="{PW}" height="{PH}" rx="14" fill="{PANEL}" stroke="{LINE}"/>')
    for i, c in enumerate((RED, AMBER, GREEN)):
        b.append(f'<circle cx="{X + 24 + i * 20}" cy="{Y + 22}" r="6" fill="{c}" opacity=".85"/>')
    b.append(t(MONO, "policy-gate  ·  12 deterministic rules  ·  fail-closed", 12.5, X + 92, Y + 27, DIM))
    b.append(f'<rect x="{X}" y="{Y + 44}" width="{PW}" height="1" fill="{LINE}"/>')
    for i, (cmd, verdict, col, why) in enumerate(CALLS):
        y = Y + 84 + i * 66
        row = t(MONO, "$", 14, X + 22, y, DIM) + t(MONO, cmd, 14, X + 40, y, INK)
        pw = MONO.width(verdict, 12.5) + 22
        row += (f'<rect x="{X + 40}" y="{y + 12}" width="{pw:.0f}" height="24" rx="6" fill="{col}" fill-opacity=".16" stroke="{col}" stroke-opacity=".55"/>'
                + t(MONO, verdict, 12.5, X + 51, y + 29, col)
                + t(MONO, why, 13, X + 40 + pw + 14, y + 29, MUT))
        b.append(fade(row, 0.6 + i * 0.7, 0.6, 8))
    return svg(W, H, "".join(b),
               "Harsh Dubey, agentic AI and LLM engineer. I build AI agents that can't be talked into the wrong action: "
               "a policy gate blocks an over-budget payment and a prompt injection, allows a read-only search, and holds a refund for human approval.")


if __name__ == "__main__":
    kit.save("banner.svg", banner())
