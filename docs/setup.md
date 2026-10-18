## Environment Setup

## Requirements

- Python 3.14.7
- Visual Studio Code
- Git
- GitHub account

## Virtual Environment

The project uses a Python virtual environment to keep dependencies separate.

Create it with:

"python -m venv .venv"

Activate it in Windows Command Prompt:

".venv\Scripts\activate.bat"

## Install Dependencies

Run:

"python -m pip install -r requirements.txt"

## Cloud Setup

Google BigQuery sandbox and Google Cloud authentication will be configured before developing the warehouse module.

## Dashboard

Power BI Desktop will be used if available on Windows. Otherwise, Looker Studio can be considered.

## goSecurity

Never commit ".env" files, cloud credentials, or secret keys.
Day 7 — BigQuery Data Validation

Validation Results

The simulated CareFlow event data was validated in Google BigQuery.

- Missing activities: 0
- Unique activities: 7
- Earliest event: 2026-09-17 08:37:00 UTC
- Latest event: 2026-10-17 07:57:00 UTC
- Schema validation: Passed — all nine columns match the Python schema.
- Data source: Simulated healthcare event data only.

Outcome

The BigQuery table "careflow_raw.raw_ehr_events" passed the activity and schema checks. The timestamp range was verified, and no missing activities were detected.

Privacy

Only simulated data is used. No real patient information or credentials are stored in the repository.