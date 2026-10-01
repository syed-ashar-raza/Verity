from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import uvicorn

from .engine import evaluate, load_cases, write_report
from .models import CaseResult, EvaluationReport, MetricResult


def read_report(path):
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return EvaluationReport(
        raw["version"],
        raw["total_cases"],
        raw["passed_cases"],
        raw["failed_cases"],
        raw["pass_rate"],
        raw["aggregate_metrics"],
        raw["latency"],
        [
            CaseResult(
                c["case_id"],
                c["passed"],
                [MetricResult(**m) for m in c["metrics"]],
                c.get("latency_ms"),
                c.get("latency_passed"),
            )
            for c in raw["cases"]
        ],
        raw["gate_passed"],
    )


def main():
    p = argparse.ArgumentParser(prog="verity")
    sub = p.add_subparsers(dest="command", required=True)
    e = sub.add_parser("evaluate")
    e.add_argument("dataset")
    e.add_argument("--output", default="verity-report.json")
    e.add_argument("--baseline")
    e.add_argument("--latency-regression", type=float, default=0.10)
    s = sub.add_parser("serve")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8000)
    a = p.parse_args()
    if a.command == "serve":
        uvicorn.run("verity.api:app", host=a.host, port=a.port)
        return
    baseline = read_report(a.baseline) if a.baseline else None
    report = evaluate(
        load_cases(a.dataset), baseline=baseline, latency_regression_pct=a.latency_regression
    )
    write_report(report, a.output)
    print(
        json.dumps(
            {
                "cases": report.total_cases,
                "passed": report.passed_cases,
                "failed": report.failed_cases,
                "pass_rate": report.pass_rate,
                "latency": report.latency,
                "gate_passed": report.gate_passed,
                "report": a.output,
            },
            indent=2,
        )
    )
    if not report.gate_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
