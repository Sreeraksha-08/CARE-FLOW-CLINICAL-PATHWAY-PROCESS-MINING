"""Compare Python bottleneck metrics with dbt/BigQuery results."""

from pathlib import Path

import pandas as pd
from google.cloud import bigquery

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYTHON_SUMMARY = PROJECT_ROOT / "analysis" / "python_bottleneck_summary.csv"

PROJECT_ID = "careflow-process-mining-511911"
SQL_TABLE = f"{PROJECT_ID}.careflow_raw.transition_time_summary"


def main():
    python_df = pd.read_csv(PYTHON_SUMMARY)

    client = bigquery.Client(project=PROJECT_ID)
    sql_df = client.query(
        f"SELECT * FROM `{SQL_TABLE}`"
    ).to_dataframe()

    keys = ["activity", "next_activity"]
    metrics = [
        "transition_count",
        "average_minutes",
        "median_minutes",
        "maximum_minutes",
    ]

    merged = python_df.merge(
        sql_df,
        on=keys,
        how="outer",
        suffixes=("_python", "_sql"),
        indicator=True,
    )

    if not (merged["_merge"] == "both").all():
        raise AssertionError("Python and SQL transition pairs differ.")

    for metric in metrics:
        left = merged[f"{metric}_python"]
        right = merged[f"{metric}_sql"]

        if metric == "transition_count":
            matches = left.astype(int).eq(right.astype(int))
        else:
            matches = (left - right).abs() <= 0.01

        if not matches.all():
            mismatches = merged.loc[
                ~matches, keys + [f"{metric}_python", f"{metric}_sql"]
            ]
            print(mismatches.to_string(index=False))
            raise AssertionError(f"Mismatch found in {metric}.")

    print(f"Compared {len(merged)} transition pairs.")
    print("PASS: Python and SQL metrics match.")


if __name__ == "__main__":
    main()