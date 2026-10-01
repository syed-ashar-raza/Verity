from __future__ import annotations

import json
import statistics
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .metrics import (
    contains,
    exact_match,
    json_structure_match,
    json_valid,
    percentile,
    token_f1,
    tool_call_correctness,
)
from .models import CaseResult, EvaluationCase, EvaluationReport, MetricResult, MetricSpec

METRICS = {
    "exact_match": exact_match,
    "contains": contains,
    "json_valid": json_valid,
    "json_structure_match": json_structure_match,
    "token_f1": token_f1,
}


def load_cases(path: str | Path) -> list[EvaluationCase]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Evaluation file must contain a JSON array.")
    return [_case_from_dict(item) for item in raw]


def _case_from_dict(item: dict[str, Any]) -> EvaluationCase:
    metrics = {
        n: MetricSpec(float(s.get("threshold", 1.0)), bool(s.get("case_sensitive", False)))
        for n, s in item.get("metrics", {}).items()
    }
    return EvaluationCase(
        id=str(item["id"]),
        input=str(item.get("input", "")),
        expected=item.get("expected"),
        prediction=item.get("prediction"),
        metrics=metrics,
        latency_ms=item.get("latency_ms"),
        max_latency_ms=item.get("max_latency_ms"),
        expected_tool_calls=item.get("expected_tool_calls"),
        actual_tool_calls=item.get("actual_tool_calls"),
    )


def evaluate_case(case: EvaluationCase) -> CaseResult:
    results = []
    for name, spec in case.metrics.items():
        if name == "tool_call_correctness":
            score = tool_call_correctness(case.expected_tool_calls, case.actual_tool_calls)
        elif name == "json_valid":
            score = json_valid(case.prediction)
        elif name == "json_structure_match":
            score = json_structure_match(case.expected, case.prediction)
        elif name == "token_f1":
            score = token_f1(str(case.expected), str(case.prediction))
        elif name in METRICS:
            score = METRICS[name](case.expected, case.prediction, spec.case_sensitive)
        else:
            raise ValueError(f"Unsupported metric: {name}")
        results.append(MetricResult(name, score, spec.threshold, score >= spec.threshold))
    latency_passed = None
    if case.max_latency_ms is not None:
        if case.latency_ms is None:
            latency_passed = False
        else:
            latency_passed = case.latency_ms <= case.max_latency_ms
        results.append(
            MetricResult(
                "latency_ms",
                case.latency_ms or 0.0,
                case.max_latency_ms,
                latency_passed,
                {"unit": "ms", "direction": "lower_is_better"},
            )
        )
    return CaseResult(
        case.id, all(r.passed for r in results), results, case.latency_ms, latency_passed
    )


def evaluate(
    cases: list[EvaluationCase],
    version="1.0.0",
    baseline: EvaluationReport | None = None,
    latency_regression_pct=0.10,
) -> EvaluationReport:
    results = [evaluate_case(c) for c in cases]
    scores: dict[str, list[float]] = {}
    latencies = []
    for r in results:
        if r.latency_ms is not None:
            latencies.append(float(r.latency_ms))
        for m in r.metrics:
            if m.name != "latency_ms":
                scores.setdefault(m.name, []).append(m.score)
    aggregate = {n: sum(v) / len(v) for n, v in scores.items()}
    latency = {}
    if latencies:
        latency = {
            "count": float(len(latencies)),
            "mean_ms": statistics.fmean(latencies),
            "p50_ms": percentile(latencies, 0.50),
            "p95_ms": percentile(latencies, 0.95),
            "max_ms": max(latencies),
        }
    passed = sum(r.passed for r in results)
    gate = passed == len(results)
    if baseline and latencies and baseline.latency:
        old = baseline.latency.get("p95_ms", 0.0)
        new = latency.get("p95_ms", 0.0)
        if old > 0 and new > old * (1 + latency_regression_pct):
            gate = False
    return EvaluationReport(
        version,
        len(results),
        passed,
        len(results) - passed,
        passed / len(results) if results else 0.0,
        aggregate,
        latency,
        results,
        gate,
    )


def write_report(report: EvaluationReport, path: str | Path) -> None:
    Path(path).write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
