"""CareFlow Day 23: Simulation Sensitivity Analysis."""

import copy
import random
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from simulator.generate_events import (
    generate_patient_journey,
    load_config,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "process_mining" / "experiments" / "day23"

PROBABILITIES = [0.10, 0.20, 0.30, 0.40, 0.50]
SEEDS = [42, 100, 200, 300, 400]
T_CRITICAL = 2.776445

def generate_dataset(probability, seed, cases, original_config):
    """Generate cases for one probability and random seed."""

    config = copy.deepcopy(original_config)
    config["scenarios"]["before"]["loopback_probability"] = probability

    rng = random.Random(seed)
    events = []

    for case_number in range(1, cases + 1):
        events.extend(
            generate_patient_journey(
                case_number,
                "before",
                config,
                rng,
            )
        )

    return pd.DataFrame(events)


def calculate_metrics(events, probability, seed):
    """Calculate observed loopback metrics."""

    case_count = events["case_id"].nunique()

    if case_count == 0:
        raise ValueError("No patient cases were generated.")

    triage_counts = events.groupby("case_id")["activity"].apply(
        lambda activities: (activities == "Triage").sum()
    )

    loopback_cases = int((triage_counts > 1).sum())

    return {
        "probability": probability,
        "seed": seed,
        "cases": case_count,
        "events": len(events),
        "loopback_cases": loopback_cases,
        "loopback_rate_percent": loopback_cases / case_count * 100,
    }


def main():
    """Run and validate all sensitivity experiments."""

    OUTPUT.mkdir(parents=True, exist_ok=True)

    original_config = load_config()
    cases = original_config["simulation"]["default_cases"]

    results = []

    print("\nCAREFLOW DAY 23")
    print("=" * 60)

    for probability in PROBABILITIES:
        for seed in SEEDS:

            events = generate_dataset(
                probability,
                seed,
                cases,
                original_config,
            )

            metrics = calculate_metrics(
                events,
                probability,
                seed,
            )

            results.append(metrics)

            filename = (
                f"probability_{int(probability * 100)}"
                f"_seed_{seed}.csv"
            )

            events.to_csv(OUTPUT / filename, index=False)

            print(
                f"Completed probability {probability:.0%}, "
                f"seed {seed}: "
                f"{metrics['loopback_rate_percent']:.2f}%"
            )

    report = pd.DataFrame(results)

    results_file = OUTPUT / "sensitivity_results.csv"
    report.to_csv(results_file, index=False)

    # Statistical summary across the five seed-level rates.
    summary_rows = []

    for probability in PROBABILITIES:
        values = report.loc[
            report["probability"] == probability,
            "loopback_rate_percent",
        ]

        mean = values.mean()
        sd = values.std(ddof=1)
        margin = T_CRITICAL * sd / (len(values) ** 0.5)

        summary_rows.append({
            "configured_probability_percent": probability * 100,
            "mean_observed_rate_percent": mean,
            "standard_deviation": sd,
            "ci_95_lower": mean - margin,
            "ci_95_upper": mean + margin,
        })

    summary = pd.DataFrame(summary_rows)

    summary_file = OUTPUT / "sensitivity_summary.csv"
    summary.to_csv(summary_file, index=False)

    # Create sensitivity-analysis graph.
    plt.figure(figsize=(9, 6))

    x = summary["configured_probability_percent"]
    y = summary["mean_observed_rate_percent"]

    lower_error = y - summary["ci_95_lower"]
    upper_error = summary["ci_95_upper"] - y

    plt.errorbar(
        x,
        y,
        yerr=[lower_error, upper_error],
        marker="o",
        capsize=5,
        label="Mean observed rate with 95% CI",
    )

    plt.plot(
        x,
        x,
        linestyle="--",
        label="Configured probability",
    )

    plt.xlabel("Configured loopback probability (%)")
    plt.ylabel("Observed loopback rate (%)")
    plt.title("CareFlow Day 23: Simulation Sensitivity Analysis")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    graph_file = OUTPUT / "sensitivity_analysis.png"
    plt.savefig(graph_file, dpi=300)
    plt.close()

    # Validate all 25 experiment datasets.
    dataset_files = list(OUTPUT.glob("probability_*_seed_*.csv"))

    assert len(report) == 25, "Expected 25 experiment results."
    assert len(dataset_files) == 25, "Expected 25 dataset files."
    assert report["cases"].eq(cases).all(), "Case count mismatch."
    assert report["loopback_rate_percent"].between(
        0, 100
    ).all(), "Invalid loopback rate."
    assert summary["ci_95_lower"].notna().all()
    assert summary["ci_95_upper"].notna().all()

    # Create project documentation.
    documentation = [
        "# CareFlow — Day 23 Sensitivity Analysis",
        "",
        "## Objective",
        "Study how configured loopback probabilities affect "
        "observed loopback rates in simulated emergency-room journeys.",
        "",
        "## Methodology",
        f"- Simulated cases per experiment: {cases}",
        f"- Configured probabilities: {', '.join(f'{p:.0%}' for p in PROBABILITIES)}",
        f"- Random seeds: {', '.join(map(str, SEEDS))}",
        "- Total experiments: 25",
        "- Each probability uses five independent seed-level runs.",
        "",
        "## Statistical summary",
        summary.to_markdown(index=False),
        "",
        "The confidence intervals are t-based 95% intervals "
        "across five seed-level observed rates per probability.",
        "",
        "## Interpretation",
        "Observed rates may differ from configured probabilities "
        "because each simulation uses a finite number of cases.",
        "The experiment measures simulator behaviour, not real "
        "hospital performance.",
        "",
        "## Outputs",
        "- sensitivity_results.csv",
        "- sensitivity_summary.csv",
        "- sensitivity_analysis.png",
        "- 25 experiment event-log CSV files",
        "",
        "## Validation",
        "All 25 experiments, case counts and loopback rates "
        "were checked by the script.",
    ]

    documentation_file = (
        ROOT / "process_mining" / "DAY23_SENSITIVITY_ANALYSIS.md"
    )

    documentation_file.write_text(
        "\n".join(documentation),
        encoding="utf-8",
    )

    print("\nSTATISTICAL SUMMARY")
    print("=" * 60)
    print(summary.round(3).to_string(index=False))

    print("\nFINAL VALIDATION")
    print("=" * 60)
    print(f"Experiments: {len(report)}")
    print(f"Dataset files: {len(dataset_files)}")
    print(f"Cases per experiment: {cases}")
    print(f"Graph: {graph_file}")
    print(f"Results: {results_file}")
    print(f"Summary: {summary_file}")
    print(f"Documentation: {documentation_file}")
    print("\nAll Day 23 checks passed!")


if __name__ == "__main__":
    main()
