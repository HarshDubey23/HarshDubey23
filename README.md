# Harsh Dubey

**Agentic AI Developer · ML Engineer · Student AI Researcher**
B.Tech, Artificial Intelligence & Machine Learning, KIET (graduating 2028)

I build AI systems where the risky parts are deterministic, and I evaluate them
the way they'd actually be used. Every number in my repositories is produced by
committed code, and every project lists its limitations.

**[Portfolio](https://iamharshdubey.vercel.app)** · **[LinkedIn](https://www.linkedin.com/in/harsh-dubey-224b08328)** · **[Email](mailto:harshdubey98190@gmail.com)**

## Selected work

| Project | What it shows | Evidence |
|---|---|---|
| **[SELLABLE](https://github.com/HarshDubey23/SELLABLE)**: agentic commerce | An AI shopping agent that structurally cannot spend money. It proposes only a SKU and quantity; 12 deterministic policy rules and a single-use approval control payment. | 578 tests · 8/8 scripted attacks blocked with 0 provider calls · **installable MCP server** |
| **[Abhed](https://github.com/HarshDubey23/hackarena)**: AI-agent governance | One gate for every action an AI agent takes, human approval for high-risk ones, and a tamper-evident signed ledger. Hackathon build, then security-audited. | [Live demo](https://kavach-os.vercel.app) · 78-case gate evaluation · [MCP server](https://github.com/HarshDubey23/abhed-mcp) |
| **[Early failure in chain-of-thought](https://github.com/HarshDubey23/early-failure-detection-cot)**: research | Where LLM reasoning errors start, and whether a detector can predict failure from part of the chain (3,400 ProcessBench solutions). Co-authored student study (KIET); I built the experiment pipeline. | Bootstrap CIs, held-out questions; modest AUROC ≈ 0.59 at 25% of the chain, reported as such |
| **[Fraud detection](https://github.com/HarshDubey23/Credit-Card-Fraud-Detection)**: ML engineering | Leakage-safe evaluation: temporal split, validation-only thresholds, cost-based operating point. | PR-AUC 0.793 [0.70, 0.88] on the last 20% of time · reproducible run · [live API](https://fraud-scoring-api.vercel.app/docs) |
| **[ProctorIQ](https://github.com/HarshDubey23/ProctorIQ)**: ML + privacy | Proctoring analytics that run in the browser (MediaPipe + 27 KB ONNX); the server re-scores events and HMAC-signs reports. | 150 backend tests · CI green · benchmark scope stated (acted clips, one webcam) · [live frontend](https://proctoriq-exam.vercel.app) |

Also: [OrderWorder](https://github.com/HarshDubey23/Resturant) (restaurant SaaS) ·
[DecodeLabs internship tasks](https://github.com/HarshDubey23/DecodeLabs_internship) ·
team contribution to [Browser-s-Agent](https://github.com/HarshDubey23/Browser-s-Agent).

## Use them from your own agent

Both agent projects ship as MCP servers that any MCP-compatible agent (Cursor, VS Code,
Windsurf and others) can use with no clone: SELLABLE runs with
`uvx --from git+https://github.com/HarshDubey23/SELLABLE sellable-mcp`, and Abhed with
`npx -y github:HarshDubey23/abhed-mcp`. Config snippets are in each repo's README.

The fraud model is a public REST API: `POST https://fraud-scoring-api.vercel.app/score`
([docs](https://fraud-scoring-api.vercel.app/docs)).

## How I work

- **Deterministic enforcement for sensitive actions:** models propose, code decides.
- **Evaluation before claims:** held-out data, baselines, confidence intervals, and failure analysis.
- **Honest results:** weak or negative findings are reported, not hidden.

## Tools

```text
Python, TypeScript · PyTorch, scikit-learn, XGBoost, ONNX Runtime, MediaPipe
FastAPI, Next.js, React · SQLite, Postgres/Supabase, MongoDB · Docker, GitHub Actions, Vercel
```

Open to agentic AI, ML engineering and research internships.
