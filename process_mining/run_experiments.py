"""Run reproducible CareFlow before-and-after experiments."""

import random
from pathlib import Path

import pandas as pd

from simulator.generate_events import (
    generate_patient_journey,
    load_config,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "process_mining" / "experiments"

SEEDS = [42, 100, 200, 300, 400]
SCENARIOS = ["before", "after"]


def generate_dataset(scenario, seed, cases, config):
    """Generate one dataset using a specified random seed."""

    rng = random.Random(seed)
    events = []

    for case_number in range(1, cases + 1):
        events.extend(
            generate_patient_journey(
                case_number,
                scenario,
                config,
                rng,
            )
        )

    return pd.DataFrame(events)


def calculate_metrics(events, scenario, seed):
    """Calculate event and loopback metrics."""

    case_count = events["case_id"].nunique()
    event_count = len(events)

    triage_counts = events.groupby("case_id")["activity"].apply(
        lambda activities: (activities == "Triage").sum()
    )

    loopback_cases = int((triage_counts > 1).sum())

    return {
        "seed": seed,
        "scenario": scenario,
        "cases": case_count,
        "events": event_count,
        "loopback_cases": loopback_cases,
        "loopback_rate_percent": (
            loopback_cases / case_count * 100
        ),
    }


def main():
    """Run all experiments and save the results."""

    config = load_config()
    cases = config["simulation"]["default_cases"]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []

    for seed in SEEDS:
        for scenario in SCENARIOS:
            events = generate_dataset(
                scenario,
                seed,
                cases,
                config,
            )

            metrics = calculate_metrics(
                events,
                scenario,
                seed,
            )

            results.append(metrics)

            output_file = (
                OUTPUT_DIR / f"{scenario}_seed_{seed}.csv"
            )

            events.to_csv(output_file, index=False)

            print(
                f"Completed {scenario} scenario "
                f"with seed {seed}"
            )

    report = pd.DataFrame(results)

    report.to_csv(
        OUTPUT_DIR / "experiment_results.csv",
        index=False,
    )

    print("\nCAREFLOW EXPERIMENT RESULTS")
    print("=" * 60)
    print(report.to_string(index=False))

    print("\nAll experiment results saved successfully.")


if __name__ == "__main__":
    main()