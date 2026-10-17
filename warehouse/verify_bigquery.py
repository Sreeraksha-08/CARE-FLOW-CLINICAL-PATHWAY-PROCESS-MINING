from google.cloud import bigquery

PROJECT_ID = "careflow-process-mining-511911"
TABLE_ID = f"{PROJECT_ID}.careflow_raw.raw_ehr_events"

client = bigquery.Client(project=PROJECT_ID)

query = f"""
SELECT
    COUNTIF(activity IS NULL OR TRIM(activity) = '') AS missing_activities,
    COUNT(DISTINCT activity) AS unique_activities,
    MIN(event_timestamp) AS earliest_event,
    MAX(event_timestamp) AS latest_event
FROM `{TABLE_ID}`
"""

for row in client.query(query).result():
    print("Missing activities:", row.missing_activities)
    print("Unique activities:", row.unique_activities)
    print("Earliest event:", row.earliest_event)
    print("Latest event:", row.latest_event)