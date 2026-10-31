import pandas as pd

from process_mining.evaluate import evaluate_scenario


def test_before_scenario_loopback_rate():
    events = pd.DataFrame({
        "case_id": ["P1", "P1", "P2", "P2", "P2"],
        "activity": [
            "Registration",
            "Triage",
            "Registration",
            "Triage",
            "Triage",
        ],
        "scenario": ["before"] * 5,
    })

    result = evaluate_scenario(events, "before", 0.40)

    assert result["cases"] == 2
    assert result["loopback_cases"] == 1
    assert result["observed_rate_percent"] == 50.0
    assert result["expected_rate_percent"] == 40.0
    assert abs(result["absolute_error_pp"] - 10.0)< 0.000001


def test_missing_scenario_returns_none():
    events = pd.DataFrame({
        "case_id": ["P1"],
        "activity": ["Registration"],
        "scenario": ["before"],
    })

    result = evaluate_scenario(events, "after", 0.03)

    assert result is None