# Harsh Dubey

**AI engineer and student researcher.** B.Tech CSE (AI & ML), KIET Group of Institutions, graduating 2028.

I build agent systems on one rule: **models propose, code decides.** The model suggests an
action; deterministic code checks it against limits a person set, and every decision is
recorded. Each number below links to the committed file that produced it, and each project
says what it doesn't do.

**[Portfolio](https://iamharshdubey.vercel.app)** · **[MCP Hub](https://iamharshdubey.vercel.app/mcp/)** · **[LinkedIn](https://www.linkedin.com/in/harsh-dubey-224b08328)** · **[Email](mailto:harshdubey98190@gmail.com)**

## Selected work

| Project | What it is | Evidence |
|---|---|---|
| **[SELLABLE](https://github.com/HarshDubey23/SELLABLE)** · [case study](https://iamharshdubey.vercel.app/work/sellable/) | A shopping agent that cannot spend money it wasn't given. It proposes only `{sku, qty}`; 12 deterministic rules and a single-use approval control payment. | 0 of 240 live-model injection attacks moved money, against 32 of 240 with a direct pay tool ([results](https://github.com/HarshDubey23/SELLABLE/blob/main/eval/llm_injection/RESULTS.md)) · 578 tests · local MCP server |
| **[Abhed](https://github.com/HarshDubey23/hackarena)** · [case study](https://iamharshdubey.vercel.app/work/abhed/) | One gate for every action an AI agent takes: allow, hold for a person, or block, on a hash-chained, signed ledger. Five-person hackathon team. | 24 of 26 malicious SDK requests blocked, 0 of 18 benign blocked ([eval](https://github.com/HarshDubey23/hackarena/blob/main/eval/RESULTS.md)) · [live demo](https://kavach-os.vercel.app) (fictional sandbox) · [MCP server](https://github.com/HarshDubey23/abhed-mcp) |
| **[Early failure in chain-of-thought](https://github.com/HarshDubey23/early-failure-detection-cot)** · [case study](https://iamharshdubey.vercel.app/work/early-failure-cot/) | Student study (KIET, co-authored; I built the experiment pipeline): where LLM reasoning errors start, and whether failure is predictable from part of the chain. Preliminary, not peer-reviewed. | AUROC 0.588 [0.552, 0.626] at 25% of the chain, a modest signal; surface features alone reach 0.618 ([results](https://github.com/HarshDubey23/early-failure-detection-cot/blob/main/docs/RESULTS.md)) |
| **[Fraud detection](https://github.com/HarshDubey23/Credit-Card-Fraud-Detection)** · [case study](https://iamharshdubey.vercel.app/work/fraud-detection/) | Leakage-safe evaluation: temporal split, thresholds chosen on validation only, a cost-based operating point. | Test PR-AUC 0.793 [0.702, 0.875]; the gain over logistic regression has a CI that includes zero ([results](https://github.com/HarshDubey23/Credit-Card-Fraud-Detection/blob/main/results/RESULTS.md)) · [live API](https://fraud-scoring-api.vercel.app/docs) |
| **[ProctorIQ](https://github.com/HarshDubey23/ProctorIQ)** · [case study](https://iamharshdubey.vercel.app/work/proctoriq/) | Proctoring analytics that run in the browser (MediaPipe and a 27 KB ONNX model); the server re-scores events and signs reports. | 99.22% on held-out acted clips from one webcam; cross-person accuracy not measured ([benchmark](https://github.com/HarshDubey23/ProctorIQ/blob/main/docs/BENCHMARK.md)) · 150 backend tests · [live Self-Test](https://proctoriq-exam.vercel.app) |

Also: team contribution to [Browser-s-Agent](https://github.com/Gauravkkaushal/Browser-s-Agent) ([case study](https://iamharshdubey.vercel.app/work/browser-agent/)) ·
[OrderWorder](https://github.com/HarshDubey23/Resturant) (restaurant SaaS) ·
[DecodeLabs internship tasks](https://github.com/HarshDubey23/DecodeLabs_internship).

## Use them from your own agent

SELLABLE and Abhed ship as **local STDIO MCP servers**: your client runs them on your computer
(Abhed's forwards each call to a hosted Abhed API). Setup for Claude Code, Claude Desktop,
Cursor, VS Code and Windsurf, with copy-ready configs, is on the
**[MCP Hub](https://iamharshdubey.vercel.app/mcp/)**. Note that VS Code's `mcp.json` uses a
`servers` key, not `mcpServers`. n8n's MCP client needs a remote HTTP server, so neither works
there.

```bash
claude mcp add sellable -- uvx --from git+https://github.com/HarshDubey23/SELLABLE sellable-mcp
claude mcp add abhed -e ABHED_AGENT_KEY=kv_live_your_key -- npx -y github:HarshDubey23/abhed-mcp
```

The fraud model is a REST API, not MCP: `POST https://fraud-scoring-api.vercel.app/score`.

## Tools

```text
Python, TypeScript · PyTorch, scikit-learn, XGBoost, ONNX Runtime, MediaPipe
FastAPI, Next.js, React · SQLite, Postgres/Supabase, MongoDB · Docker, GitHub Actions, Vercel
```

Open to agentic AI, ML engineering and research internships.
