from __future__ import annotations

import json
from collections import Counter
from typing import Any


def normalize(value: Any, case_sensitive: bool = False) -> str:
    text = str(value).strip()
    return text if case_sensitive else text.casefold()


def exact_match(expected: Any, prediction: Any, case_sensitive: bool = False) -> float:
    return float(normalize(expected, case_sensitive) == normalize(prediction, case_sensitive))


def contains(expected: Any, prediction: Any, case_sensitive: bool = False) -> float:
    return float(normalize(expected, case_sensitive) in normalize(prediction, case_sensitive))


def json_valid(prediction: Any) -> float:
    if not isinstance(prediction, str):
        return 0.0
    try:
        json.loads(prediction)
        return 1.0
    except (TypeError, ValueError):
        return 0.0


def json_structure_match(expected: Any, prediction: Any) -> float:
    try:
        e = json.loads(expected) if isinstance(expected, str) else expected
        p = json.loads(prediction) if isinstance(prediction, str) else prediction
    except (TypeError, ValueError):
        return 0.0
    if not isinstance(e, dict) or not isinstance(p, dict):
        return 0.0
    return float(set(e) == set(p))


def tool_call_correctness(expected, actual) -> float:
    if expected is None or actual is None or len(expected) != len(actual):
        return 0.0
    return float(all(e == a for e, a in zip(expected, actual, strict=True)))


def token_f1(expected: str, prediction: str) -> float:
    e = normalize(expected).split()
    p = normalize(prediction).split()
    if not e or not p:
        return 0.0
    overlap = sum((Counter(e) & Counter(p)).values())
    precision = overlap / len(p)
    recall = overlap / len(e)
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * p
    lo = int(rank)
    hi = min(lo + 1, len(ordered) - 1)
    return round(ordered[lo] + (ordered[hi] - ordered[lo]) * (rank - lo), 10)
