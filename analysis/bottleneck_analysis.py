"""Analyze time between consecutive CareFlow activities."""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "sample_data" / "before_events_with_attributes_recent.csv"
OUTPUT_PATH = PROJECT_ROOT / "analysis" / "python_bottleneck_summary.csv"


def main():
    events = pd.read_csv(DATA_PATH)

    required = {"case_id", "activity", "timestamp"}
    missing = required - set(events.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    events["timestamp"] = pd.to_datetime(
        events["timestamp"], errors="raise"
    )

    events = events.sort_values(
        ["case_id", "timestamp"]
    ).copy()

    events["next_activity"] = (
        events.groupby("case_id")["activity"].shift(-1)
    )
    events["next_timestamp"] = (
        events.groupby("case_id")["timestamp"].shift(-1)
    )

    events["transition_minutes"] = (
        events["next_timestamp"] - events["timestamp"]
    ).dt.total_seconds() / 60

    transitions = events.dropna(
        subset=["next_activity", "next_timestamp"]
    ).copy()

    summary = (
        transitions.groupby(
            ["activity", "next_activity"], as_index=False
        )
        .agg(
            transition_count=("transition_minutes", "count"),
            average_minutes=("transition_minutes", "mean"),
            median_minutes=("transition_minutes", "median"),
            maximum_minutes=("transition_minutes", "max"),
        )
        .sort_values("average_minutes", ascending=False)
    )

    summary[
        ["average_minutes", "median_minutes", "maximum_minutes"]
    ] = summary[
        ["average_minutes", "median_minutes", "maximum_minutes"]
    ].round(2)

    summary.to_csv(OUTPUT_PATH, index=False)

    print(f"Cases: {events['case_id'].nunique()}")
    print(f"Transitions analyzed: {len(transitions)}")
    print("\nTop 10 transitions by average time:")
    print(summary.head(10).to_string(index=False))
    print(f"\nSaved summary to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()