from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MetricSpec:
    threshold: float = 1.0
    case_sensitive: bool = False


@dataclass(frozen=True)
class EvaluationCase:
    id: str
    input: str
    expected: Any
    prediction: Any
    metrics: dict[str, MetricSpec] = field(default_factory=dict)
    latency_ms: float | None = None
    max_latency_ms: float | None = None
    expected_tool_calls: list[dict[str, Any]] | None = None
    actual_tool_calls: list[dict[str, Any]] | None = None


@dataclass(frozen=True)
class MetricResult:
    name: str
    score: float
    threshold: float
    passed: bool
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    passed: bool
    metrics: list[MetricResult]
    latency_ms: float | None = None
    latency_passed: bool | None = None


@dataclass(frozen=True)
class EvaluationReport:
    version: str
    total_cases: int
    passed_cases: int
    failed_cases: int
    pass_rate: float
    aggregate_metrics: dict[str, float]
    latency: dict[str, float]
    cases: list[CaseResult]
    gate_passed: bool
