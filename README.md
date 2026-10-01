# Verity

### AI Evaluation & Regression Platform

[![CI](https://github.com/syed-ashar-raza/Verity/actions/workflows/ci.yml/badge.svg)](https://github.com/syed-ashar-raza/Verity/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production%20API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue)](LICENSE)

**Verity is a production-oriented evaluation and regression platform for AI systems.**

It provides deterministic evaluation metrics, per-case thresholds, latency budgets, statistical latency reporting, baseline regression gates, JSON evaluation reports, a FastAPI service, and a CLI designed for repeatable quality checks in CI.

> **Core principle:** AI quality gates should be reproducible, measurable, and reviewable.

---

## Why Verity?

AI systems can appear to work while silently degrading in correctness, latency, structured output, or tool execution.

Verity turns those requirements into explicit evaluation cases and machine-readable quality gates.

### Evaluation Flow

    AI System
        |
        v
    Evaluation Dataset
        |
        +-- Correctness
        +-- Structured Output
        +-- Tool Calls
        +-- Latency
        +-- Thresholds
        |
        v
    Evaluation Engine
        |
        +-- Case Results
        +-- p50 / p95 / max latency
        +-- Regression Gate
        |
        v
    JSON Report -----> CI Artifact

---

## Features

### Deterministic Evaluation

- Exact-match evaluation
- Containment evaluation
- Token-F1
- JSON validity checks
- JSON structure checks
- Tool-call correctness
- Per-case thresholds

### Performance Evaluation

- Latency budgets
- Mean latency
- p50 latency
- p95 latency
- Maximum latency
- Baseline p95 regression detection

### Engineering Interface

- Python evaluation engine
- FastAPI REST API
- CLI
- JSON evaluation reports
- pytest test suite
- Ruff linting and formatting
- Docker support
- GitHub Actions CI
- CI evaluation artifacts

---

## Verified Evaluation

Verity was executed against its included example evaluation dataset.

| Metric | Result |
|---|---:|
| Evaluation cases | 5 |
| Passed | 5 |
| Failed | 0 |
| Pass rate | **100%** |
| Mean latency | **142 ms** |
| p50 latency | **142 ms** |
| p95 latency | **142 ms** |
| Maximum latency | **142 ms** |
| Regression gate | **PASSED** |

> These measurements represent the included local example evaluation dataset, not production traffic.

---

## Evaluation Model

Each evaluation case explicitly defines what should be measured.

Example:

    {
      "id": "exact-answer",
      "input": "What is 2 + 2?",
      "expected": "4",
      "prediction": "4",
      "metrics": {
        "exact_match": {
          "threshold": 1.0
        }
      }
    }

The engine evaluates the case and produces a structured result.

A quality gate fails when:

1. A required evaluation case fails.
2. A metric falls below its configured threshold.
3. A candidate p95 latency exceeds the permitted baseline tolerance.

This makes evaluation suitable for automated CI checks.

---

## Supported Metrics

| Metric | Purpose |
|---|---|
| Exact Match | Exact deterministic answer comparison |
| Contains | Checks whether expected content appears in the prediction |
| Token-F1 | Token-level precision/recall based similarity |
| JSON Validity | Validates JSON output |
| JSON Structure | Compares expected and predicted JSON structure |
| Tool-Call Correctness | Validates expected vs actual tool calls |

Verity intentionally keeps the core evaluation layer deterministic.

It does **not** fabricate subjective LLM-judge scores.

Model-based evaluators can be integrated later when the evaluator model, prompt, dataset, and reproducibility requirements are explicitly controlled.

---

## Latency Regression

Verity records latency for evaluated cases and calculates:

- Mean
- p50
- p95
- Maximum

A baseline report can be supplied to detect performance regressions.

This allows an AI system to be evaluated on both correctness and performance:

    Correctness
         +
    Performance
         |
         v
     Quality Gate

---

## CLI

### Create the Environment

    py -3.14 -m venv .venv
    .\.venv\Scripts\Activate.ps1

### Install

    python -m pip install -e ".[dev]"

### Run an Evaluation

    verity evaluate examples/cases.json --output verity-report.json

### Run Tests

    pytest

### Run Linting

    ruff check .

### Start the API

    verity serve

---

## API

### Health

    GET /health

### Evaluate

    POST /v1/evaluate

The API accepts evaluation cases and returns structured evaluation results.

---

## CI

Every push and pull request runs the Verity quality pipeline:

    Checkout
        |
        v
    Python 3.14
        |
        v
    Install
        |
        +-- Ruff
        +-- pytest
        +-- Verity evaluation
                |
                v
        JSON evaluation artifact

The CI workflow is defined in:

    .github/workflows/ci.yml

The evaluation report is uploaded as a GitHub Actions artifact.

---

## Project Structure

    Verity/
    |
    +-- .github/
    |   +-- workflows/
    |       +-- ci.yml
    |
    +-- docs/
    |   +-- evaluation.md
    |
    +-- examples/
    |   +-- cases.json
    |
    +-- src/
    |   +-- verity/
    |       +-- api.py
    |       +-- cli.py
    |       +-- engine.py
    |       +-- metrics.py
    |       +-- models.py
    |
    +-- tests/
    |   +-- test_api.py
    |   +-- test_engine.py
    |   +-- test_metrics.py
    |
    +-- Dockerfile
    +-- docker-compose.yml
    +-- pyproject.toml
    +-- README.md

---

## Engineering Design

Verity separates evaluation concerns into focused components:

    Models
       |
       v
    Metrics
       |
       v
    Evaluation Engine
       |
       +-- CLI
       |
       +-- FastAPI
              |
              v
          JSON Reports

This separation allows evaluation logic to be reused from both the command line and HTTP API without duplicating the core evaluation implementation.

---

## Quality Evidence

Current local verification:

    pytest
    5 passed

    ruff check .
    All checks passed!

    verity evaluate examples/cases.json

    5 cases
    5 passed
    0 failed
    100% pass rate
    gate_passed: true

The generated evaluation report is:

    verity-report.json

---

## Docker

Build and run the service with:

    docker compose up --build

The containerized service exposes the FastAPI application.

---

## Scope

Verity v1.0.0 focuses on deterministic evaluation and regression infrastructure.

It deliberately avoids:

- Fabricated benchmark claims
- Subjective scores without reproducible evaluators
- Hidden evaluation logic
- Unnecessary model-specific coupling

The architecture is intentionally designed so additional evaluators can be introduced without replacing the core evaluation engine.

---

## Roadmap

Potential future extensions include:

- Retrieval metrics such as Recall@K and MRR
- Token and cost budgets
- Additional structured-output validators
- Dataset versioning
- Model-based evaluators with reproducibility controls
- More advanced regression policies

These are future extensions, not claims about the current v1.0.0 implementation.

---

## License

Apache-2.0