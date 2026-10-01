from verity.metrics import (
    contains,
    exact_match,
    json_structure_match,
    json_valid,
    percentile,
    token_f1,
    tool_call_correctness,
)


def test_metrics():
    assert exact_match("Paris", "paris") == 1.0
    assert contains("30 days", "Refunds are available for 30 days.") == 1.0
    assert json_valid('{"name":"Ashar"}') == 1.0
    assert json_structure_match('{"name":"Ashar"}', '{"name":"Other"}') == 1.0
    assert (
        tool_call_correctness(
            [{"name": "search", "arguments": {"q": "AI"}}],
            [{"name": "search", "arguments": {"q": "AI"}}],
        )
        == 1.0
    )
    assert token_f1("fast reliable API", "fast reliable API") == 1.0
    assert percentile([1, 2, 3, 4], 0.95) == 3.85
