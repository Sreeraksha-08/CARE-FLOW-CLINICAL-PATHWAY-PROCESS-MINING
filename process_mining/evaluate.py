"""Validate CareFlow simulator loopback outcomes."""

from pathlib import Path

import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_PATH = PROJECT_ROOT / "simulator" / "config.yaml"

BEFORE_PATH = (
    PROJECT_ROOT
    / "process_mining"
    / "outputs"
    / "careflow_event_log.csv"
)

AFTER_PATH = (
    PROJECT_ROOT
    / "sample_data"
    / "after_events_validation.csv"
)


def load_config():
    """Load expected loopback probabilities."""
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def evaluate_scenario(events, scenario, expected_probability):
    """Calculate observed loopback rate for each patient scenario."""

    subset = events[events["scenario"] == scenario]

    if subset.empty:
        return None

    case_count = subset["case_id"].nunique()

    activity_counts = (
        subset.groupby("case_id")["activity"]
        .apply(lambda activities: (activities == "Triage").sum())
    )

    loopback_cases = int((activity_counts > 1).sum())
    observed_rate = loopback_cases / case_count

    return {
        "scenario": scenario,
        "cases": case_count,
        "loopback_cases": loopback_cases,
        "expected_rate_percent": expected_probability * 100,
        "observed_rate_percent": observed_rate * 100,
        "absolute_error_pp": abs(
            observed_rate - expected_probability
        ) * 100,
    }


def main():
    config = load_config()

    datasets = {
        "before": BEFORE_PATH,
        "after": AFTER_PATH,
    }

    results = []

    for scenario, file_path in datasets.items():
        if not file_path.exists():
            print(f"Skipping {scenario}: file not found.")
            continue

        events = pd.read_csv(file_path)

        required_columns = {"case_id", "activity", "scenario"}
        missing_columns = required_columns - set(events.columns)

        if missing_columns:
            raise ValueError(
                f"Missing columns: {sorted(missing_columns)}"
            )

        expected_probability = config["scenarios"][scenario][
            "loopback_probability"
        ]

        result = evaluate_scenario(
            events,
            scenario,
            expected_probability,
        )

        if result is not None:
            results.append(result)

    if not results:
        print("No scenarios available for evaluation.")
        return

    report = pd.DataFrame(results)

    print("\nCAREFLOW GROUND-TRUTH VALIDATION")
    print("=" * 65)
    print(
        report.to_string(
            index=False,
            float_format=lambda value: f"{value:.2f}",
        )
    )

    print("\nError = absolute difference in percentage points.")
    print("Results describe simulated data only.")


if __name__ == "__main__":
    main()