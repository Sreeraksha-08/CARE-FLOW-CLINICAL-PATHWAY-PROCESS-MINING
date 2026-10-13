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

## Security

Never commit ".env" files, cloud credentials, or secret keys.