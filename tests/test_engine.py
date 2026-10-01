from dataclasses import replace

from verity.engine import evaluate, load_cases


def test_dataset_passes():
    report = evaluate(load_cases("examples/cases.json"))
    assert (report.total_cases, report.passed_cases, report.failed_cases) == (5, 5, 0)
    assert report.pass_rate == 1.0 and report.gate_passed


def test_failed_case_closes_gate():
    case = load_cases("examples/cases.json")[0]
    assert not evaluate([replace(case, prediction="London")]).gate_passed
