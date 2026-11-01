"""Compare final simulated CareFlow before-and-after scenarios."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "sample_data" / "final"
OUTPUT_DIR = ROOT / "analysis" / "final_outputs"

SCENARIOS = {
    "before": DATA_DIR / "before_events_final.csv",
    "after": DATA_DIR / "after_events_final.csv",
}


def load_scenario(name: str, path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing dataset: {path}")

    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")

    return df.sort_values(
        ["case_id", "timestamp"],
        kind="stable",
    )


def summarize_scenario(name: str, df: pd.DataFrame) -> dict:
    case_summary = df.groupby("case_id").agg(
        total_events=("activity", "size"),
        pathway_start=("timestamp", "min"),
        pathway_end=("timestamp", "max"),
        triage_events=("activity", lambda values: (values == "Triage").sum()),
    )

    case_summary["duration_minutes"] = (
        case_summary["pathway_end"] - case_summary["pathway_start"]
    ).dt.total_seconds() / 60

    loopback_cases = int((case_summary["triage_events"] > 1).sum())
    total_cases = int(case_summary.shape[0])

    return {
        "scenario": name,
        "patient_cases": total_cases,
        "total_events": int(len(df)),
        "loopback_cases": loopback_cases,
        "loopback_rate_percent": round(
            loopback_cases / total_cases * 100, 2
        ) if total_cases else 0,
        "average_pathway_duration_minutes": round(
            case_summary["duration_minutes"].mean(), 2
        ),
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    frames = {
        name: load_scenario(name, path)
        for name, path in SCENARIOS.items()
    }

    summary = pd.DataFrame(
        [
            summarize_scenario(name, df)
            for name, df in frames.items()
        ]
    )

    summary.to_csv(
        OUTPUT_DIR / "scenario_comparison.csv",
        index=False,
    )

    activity_summary = pd.concat(
        [
            df.groupby("activity").size().rename(name)
            for name, df in frames.items()
        ],
        axis=1,
    ).fillna(0).astype(int)

    activity_summary.index.name = "activity"
    activity_summary.to_csv(
        OUTPUT_DIR / "activity_comparison.csv"
    )

    print("Scenario comparison files created.")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()