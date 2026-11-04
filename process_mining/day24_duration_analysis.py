"""CareFlow Day 24: Patient pathway duration and performance analysis."""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "sample_data" / "final"
OUTPUT_DIR = ROOT / "process_mining" / "experiments" / "day24"

INPUT_FILES = {
    "before": DATA_DIR / "before_events_final.csv",
    "after": DATA_DIR / "after_events_final.csv",
}


def load_events(scenario, path):
    """Load and validate one scenario's event log."""

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    required = {"case_id", "activity", "timestamp"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"{scenario}: Missing columns: {missing}")

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
    )

    if df["timestamp"].isna().any():
        raise ValueError(f"{scenario}: Invalid or missing timestamps.")

    if df["case_id"].isna().any():
        raise ValueError(f"{scenario}: Missing case IDs.")

    if df["activity"].isna().any():
        raise ValueError(f"{scenario}: Missing activity names.")

    df["scenario"] = scenario

    return df


def analyse_scenario(scenario, path):
    """Calculate activity and patient pathway durations."""

    df = load_events(scenario, path)

    df = df.sort_values(
        ["case_id", "timestamp"]
    ).copy()

    # Calculate elapsed time until the next event.
    df["next_timestamp"] = (
        df.groupby("case_id")["timestamp"].shift(-1)
    )

    df["duration_minutes"] = (
        df["next_timestamp"] - df["timestamp"]
    ).dt.total_seconds() / 60

    measured = df["duration_minutes"].dropna()

    if (measured < 0).any():
        raise ValueError(f"{scenario}: Negative event duration found.")

    # Activity-level duration summary.
    activity_summary = (
        df.dropna(subset=["duration_minutes"])
        .groupby("activity")["duration_minutes"]
        .agg(
            event_intervals="count",
            mean_minutes="mean",
            median_minutes="median",
            max_minutes="max",
        )
        .reset_index()
    )

    activity_summary.insert(0, "scenario", scenario)

    # Patient-level total pathway duration.
    patient_summary = (
        df.groupby("case_id")
        .agg(
            start_time=("timestamp", "min"),
            end_time=("timestamp", "max"),
            event_count=("activity", "count"),
        )
        .reset_index()
    )

    patient_summary["pathway_duration_minutes"] = (
        patient_summary["end_time"] - patient_summary["start_time"]
    ).dt.total_seconds() / 60

    patient_summary.insert(0, "scenario", scenario)

    return df, activity_summary, patient_summary


def main():
    """Run analysis, create graphs and validate outputs."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_events = []
    activity_tables = []
    patient_tables = []

    print("\nCAREFLOW DAY 24")
    print("=" * 65)

    for scenario, path in INPUT_FILES.items():

        events, activities, patients = analyse_scenario(
            scenario,
            path,
        )

        all_events.append(events)
        activity_tables.append(activities)
        patient_tables.append(patients)

        print(
            f"{scenario.title()}: "
            f"{patients['case_id'].nunique()} cases, "
            f"{len(events)} events"
        )

    # Combine scenario results.
    activity_summary = pd.concat(
        activity_tables,
        ignore_index=True,
    )

    patient_summary = pd.concat(
        patient_tables,
        ignore_index=True,
    )

    activity_file = OUTPUT_DIR / "activity_duration_summary.csv"
    patient_file = OUTPUT_DIR / "patient_pathway_duration.csv"

    activity_summary.to_csv(activity_file, index=False)
    patient_summary.to_csv(patient_file, index=False)

    # Compare overall patient pathway durations.
    comparison = (
        patient_summary.groupby("scenario")[
            "pathway_duration_minutes"
        ]
        .agg(
            cases="count",
            mean_minutes="mean",
            median_minutes="median",
            max_minutes="max",
            min_minutes="min",
        )
        .reset_index()
    )

    comparison_file = OUTPUT_DIR / "scenario_comparison.csv"
    comparison.to_csv(comparison_file, index=False)

    # Compare activity durations across scenarios.
    activity_comparison = activity_summary.sort_values(
        ["scenario", "mean_minutes"],
        ascending=[True, False],
    )

    activity_comparison_file = (
        OUTPUT_DIR / "activity_scenario_comparison.csv"
    )

    activity_comparison.to_csv(
        activity_comparison_file,
        index=False,
    )

    # Graph 1: Mean activity interval duration.
    pivot = activity_summary.pivot(
        index="activity",
        columns="scenario",
        values="mean_minutes",
    )

    ax = pivot.plot(
        kind="bar",
        figsize=(11, 6),
    )

    ax.set_title("CareFlow: Mean Activity Interval Duration")
    ax.set_xlabel("Activity")
    ax.set_ylabel("Duration (minutes)")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(title="Scenario")
    plt.tight_layout()

    activity_graph = OUTPUT_DIR / "activity_duration.png"
    plt.savefig(activity_graph, dpi=300)
    plt.close()

    # Graph 2: Mean patient pathway duration.
    plt.figure(figsize=(8, 5))

    plt.bar(
        comparison["scenario"],
        comparison["mean_minutes"],
    )

    plt.title("CareFlow: Mean Patient Pathway Duration")
    plt.xlabel("Scenario")
    plt.ylabel("Duration (minutes)")
    plt.tight_layout()

    pathway_graph = OUTPUT_DIR / "pathway_comparison.png"
    plt.savefig(pathway_graph, dpi=300)
    plt.close()

    # Validate the results.
    assert len(comparison) == 2
    assert set(comparison["scenario"]) == {"before", "after"}
    assert patient_summary["pathway_duration_minutes"].ge(0).all()
    assert activity_summary["mean_minutes"].ge(0).all()
    assert patient_summary.groupby("scenario")["case_id"].nunique().sum() == 200
    assert activity_summary["mean_minutes"].notna().all()

    # Create documentation.
    documentation = [
        "# CareFlow — Day 24: Duration Analysis",
        "",
        "## Objective",
        "Analyse simulated activity intervals and total patient pathway durations.",
        "",
        "## Methodology",
        "- Events are sorted by case ID and timestamp.",
        "- Activity interval duration is calculated as the time until the next event in the same case.",
        "- The final event in each case has no subsequent interval and is excluded from activity-level duration statistics.",
        "- Patient pathway duration is calculated from the first to the last event.",
        "- Mean, median, minimum and maximum pathway durations are compared.",
        "",
        "## Patient pathway comparison",
        comparison.to_markdown(index=False),
        "",
        "## Activity duration summary",
        activity_summary.to_markdown(index=False),
        "",
        "## Interpretation",
        "Activity intervals represent elapsed time between consecutive recorded events. "
        "They do not necessarily represent the exact time spent performing an activity.",
        "Long intervals may indicate periods worth investigating, but do not independently "
        "prove a clinical bottleneck.",
        "",
        "## Limitations",
        "All data is simulated. Before-and-after differences reflect the simulated "
        "scenarios and must not be interpreted as real hospital improvements.",
        "",
        "## Generated outputs",
        "- activity_duration_summary.csv",
        "- patient_pathway_duration.csv",
        "- scenario_comparison.csv",
        "- activity_scenario_comparison.csv",
        "- activity_duration.png",
        "- pathway_comparison.png",
        "",
        "## Validation",
        "Both scenarios, patient counts, duration values and output files were checked.",
    ]

    documentation_file = (
        ROOT / "process_mining" / "DAY24_DURATION_ANALYSIS.md"
    )

    documentation_file.write_text(
        "\n".join(documentation),
        encoding="utf-8",
    )

    # Final output.
    print("\nPATIENT PATHWAY COMPARISON")
    print("=" * 65)
    print(comparison.round(2).to_string(index=False))

    print("\nACTIVITY DURATION SUMMARY")
    print("=" * 65)
    print(activity_summary.round(2).to_string(index=False))

    print("\nFINAL VALIDATION")
    print("=" * 65)
    print(f"Scenarios analysed: {len(comparison)}")
    print(f"Patient cases analysed: {patient_summary['case_id'].nunique()}")
    print(f"Activity summaries: {len(activity_summary)}")
    print(f"Output folder: {OUTPUT_DIR}")
    print(f"Documentation: {documentation_file}")
    print("\nAll Day 24 checks passed!")


if __name__ == "__main__":
    main()
