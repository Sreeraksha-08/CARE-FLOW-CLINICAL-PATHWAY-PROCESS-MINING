"""Load simulated CareFlow events into the BigQuery raw table."""

import argparse
import uuid

import pandas as pd
from google.cloud import bigquery

from schema import PROJECT_ID, DATASET_ID, TABLE_ID


def load_events(csv_path: str, replace: bool = False) -> None:
    df = pd.read_csv(csv_path)

    required_columns = {
        "case_id",
        "activity",
        "timestamp",
        "scenario",
        "loopback_reason",
    }
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

    # Convert the CSV columns to the BigQuery table schema.
    events = pd.DataFrame(
        {
            "event_id": [str(uuid.uuid4()) for _ in range(len(df))],
            "case_id": df["case_id"].astype(str),
            "activity": df["activity"],
            "event_timestamp": pd.to_datetime(df["timestamp"], errors="coerce"),
            "resource": None,
            "department": None,
            "age_group": None,
            "loopback_reason": df["loopback_reason"].where(
                df["loopback_reason"].notna(), None
            ),
            "scenario": df["scenario"],
        }
    )

    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        write_disposition=(
            bigquery.WriteDisposition.WRITE_TRUNCATE
            if replace
            else bigquery.WriteDisposition.WRITE_APPEND
        ),
        schema=[
            bigquery.SchemaField("event_id", "STRING"),
            bigquery.SchemaField("case_id", "STRING"),
            bigquery.SchemaField("activity", "STRING"),
            bigquery.SchemaField("event_timestamp", "TIMESTAMP"),
            bigquery.SchemaField("resource", "STRING"),
            bigquery.SchemaField("department", "STRING"),
            bigquery.SchemaField("age_group", "STRING"),
            bigquery.SchemaField("loopback_reason", "STRING"),
            bigquery.SchemaField("scenario", "STRING"),
        ],
    )

    job = client.load_table_from_dataframe(
        events, table_id, job_config=job_config
    )
    job.result()

    table = client.get_table(table_id)
    print(f"Loaded {len(events)} events into {table_id}")
    print(f"Total rows currently in table: {table.num_rows}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv",
        default="sample_data/before_events.csv",
        help="Path to the simulated event CSV",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace existing table contents instead of appending",
    )
    args = parser.parse_args()

    load_events(args.csv, replace=args.replace)