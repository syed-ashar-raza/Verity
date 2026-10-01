from __future__ import annotations

from dataclasses import asdict
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .engine import evaluate
from .models import EvaluationCase, MetricSpec

app = FastAPI(title="Verity", version="1.0.0")


class CaseRequest(BaseModel):
    id: str
    input: str = ""
    expected: Any = None
    prediction: Any = None
    metrics: dict[str, MetricSpec] = Field(default_factory=dict)
    latency_ms: float | None = None
    max_latency_ms: float | None = None
    expected_tool_calls: list[dict[str, Any]] | None = None
    actual_tool_calls: list[dict[str, Any]] | None = None


class EvaluationRequest(BaseModel):
    cases: list[CaseRequest] = Field(min_length=1)
    latency_regression_pct: float = Field(default=0.10, ge=0)


@app.get("/health")
def health():
    return {"status": "ok", "service": "verity", "version": "1.0.0"}


@app.post("/v1/evaluate")
def run_evaluation(request: EvaluationRequest):
    try:
        cases = [
            EvaluationCase(
                id=c.id,
                input=c.input,
                expected=c.expected,
                prediction=c.prediction,
                metrics=c.metrics,
                latency_ms=c.latency_ms,
                max_latency_ms=c.max_latency_ms,
                expected_tool_calls=c.expected_tool_calls,
                actual_tool_calls=c.actual_tool_calls,
            )
            for c in request.cases
        ]
        return asdict(evaluate(cases, latency_regression_pct=request.latency_regression_pct))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
