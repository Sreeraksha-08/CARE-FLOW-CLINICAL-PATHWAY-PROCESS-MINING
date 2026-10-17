"""BigQuery schema definitions for the CareFlow project."""

PROJECT_ID = "careflow-process-mining-511911"
DATASET_ID = "careflow_raw"
TABLE_ID = "raw_ehr_events"

TABLE_SCHEMA = [
	{"name": "event_id", "type": "STRING", "mode": "NULLABLE"},
	{"name": "case_id", "type": "STRING", "mode": "NULLABLE"},
	{"name": "activity", "type": "STRING", "mode": "NULLABLE"},
	{"name": "event_timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"},
	{"name": "resource", "type": "STRING", "mode": "NULLABLE"},
	{"name": "department", "type": "STRING", "mode": "NULLABLE"},
	{"name": "age_group", "type": "STRING", "mode": "NULLABLE"},
	{"name": "loopback_reason", "type": "STRING", "mode": "NULLABLE"},
	{"name": "scenario", "type": "STRING", "mode": "NULLABLE"},
]

TABLE_FQN = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
