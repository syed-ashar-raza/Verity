# Verity

**Verity v1.0.0 — AI Evaluation & Regression Platform**

A production-oriented evaluation service for reproducible AI-system tests, deterministic metrics,
latency budgets, thresholds, and regression gates.

## Features

- Exact-match, containment, token-F1 metrics
- JSON validity and structure checks
- Tool-call correctness
- Latency budgets and p50/p95 statistics
- Baseline latency regression gate
- JSON reports for CI artifacts
- FastAPI API and CLI
- pytest, Ruff, Docker, GitHub Actions

Verity deliberately does not fabricate subjective LLM-judge scores. Model-based evaluators can be
added behind the same evaluation architecture when a pinned evaluator and reproducible dataset exist.

## Quick start

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
verity evaluate examples/cases.json --output verity-report.json
pytest
ruff check .
verity serve
```

API: `GET /health`, `POST /v1/evaluate`.

## Evaluation principle

A quality gate should be reproducible. Each case declares its metric and threshold. CI fails when a
case fails or a candidate's p95 latency exceeds the baseline tolerance.

## License

Apache-2.0
