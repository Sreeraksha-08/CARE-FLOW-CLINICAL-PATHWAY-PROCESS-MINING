"""Prepare consistent final before-and-after CareFlow datasets."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "sample_data"
OUTPUT_DIR = DATA_DIR / "final"

FILES = {
    "before": DATA_DIR / "before_events_with_attributes.csv",
    "after": DATA_DIR / "after_events_validation.csv",
}

REQUIRED_COLUMNS = [
    "case_id",
    "activity",
    "timestamp",
    "scenario",
    "loopback_reason",
    "age_group",
    "department",
    "resource",
]

EXPECTED_ACTIVITIES = {
    "Registration",
    "Triage",
    "Doctor Consultation",
    "X-Ray",
    "Doctor Review",
    "Lab Test",
    "Discharge",
}


def prepare_dataset(name: str, source: Path) -> pd.DataFrame:
    if not source.exists():
        raise FileNotFoundError(f"Dataset not found: {source}")

    df = pd.read_csv(source)

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(f"{name}: missing columns {sorted(missing_columns)}")

    df = df[REQUIRED_COLUMNS].copy()

    df["case_id"] = df["case_id"].astype("string").str.strip()
    df["activity"] = df["activity"].astype("string").str.strip()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    actual_activities = set(df["activity"].dropna().unique())
    unexpected = actual_activities - EXPECTED_ACTIVITIES

    if unexpected:
        raise ValueError(
            f"{name}: unexpected activity names {sorted(unexpected)}"
        )

    if df["case_id"].isna().any() or df["activity"].isna().any():
        raise ValueError(f"{name}: missing case IDs or activity names")

    if df["timestamp"].isna().any():
        raise ValueError(f"{name}: invalid or missing timestamps")

    df = df.sort_values(
        ["case_id", "timestamp"],
        kind="stable",
    ).reset_index(drop=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / f"{name}_events_final.csv"

    df.to_csv(output, index=False)

    print(f"{name.title()} dataset saved: {output}")
    print(f"Cases: {df['case_id'].nunique()}")
    print(f"Events: {len(df)}")

    return df


def main() -> None:
    before = prepare_dataset("before", FILES["before"])
    after = prepare_dataset("after", FILES["after"])

    if list(before.columns) != list(after.columns):
        raise ValueError("Before and after schemas do not match")

    print("\nFinal dataset preparation completed.")
    print("Original source files were not modified.")


if __name__ == "__main__":
    main()