"""Validate CareFlow transition-time calculations."""

import pandas as pd

from analysis.bottleneck_analysis import DATA_PATH


def test_transition_metrics_are_valid():
    events = pd.read_csv(DATA_PATH)

    events["timestamp"] = pd.to_datetime(
        events["timestamp"], errors="raise"
    )
    events = events.sort_values(["case_id", "timestamp"]).copy()

    events["next_activity"] = (
        events.groupby("case_id")["activity"].shift(-1)
    )
    events["next_timestamp"] = (
        events.groupby("case_id")["timestamp"].shift(-1)
    )

    transitions = events.dropna(
        subset=["next_activity", "next_timestamp"]
    ).copy()

    transitions["transition_minutes"] = (
        transitions["next_timestamp"] - transitions["timestamp"]
    ).dt.total_seconds() / 60

    assert len(transitions) == 568
    assert transitions["transition_minutes"].notna().all()
    assert (transitions["transition_minutes"] >= 0).all()
    assert transitions["case_id"].nunique() == 100