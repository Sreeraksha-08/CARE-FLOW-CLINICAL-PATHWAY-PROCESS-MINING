# CareFlow — Project Configuration

## 1. Runtime Environment

- Operating system used during development: Windows
- Shell: PowerShell
- Programming language: Python
- Virtual environment: ".venv"

## 2. Python Dependencies

Install packages using the repository's "requirements.txt":

pip install -r requirements.txt

## 3. Simulation Configuration

The simulator uses configurable parameters for:

- Number of patient cases
- Random seed
- Clinical activity sequences
- Repeated activity probabilities
- Patient attributes
- Scenario settings

The simulator configuration is maintained in the "simulator/" directory.

## 4. BigQuery Configuration

The warehouse workflow uses:

- Google Cloud project configuration
- BigQuery dataset and table settings
- Google Cloud authentication

Never commit service-account keys, private credentials or ".env" files.

## 5. dbt Configuration

The dbt project is maintained in "dbt_project/".

Run dbt commands from the configured project directory and ensure the BigQuery profile is correctly configured.

## 6. Dashboard Configuration

The Streamlit application is located at:

"dashboard/app.py"

The dashboard reads process-mining outputs and final scenario comparison files.

## 7. Reproducibility

Results depend on the selected simulation settings, random seed and input datasets.

## 8. Data Scope

All patient records are simulated. No real patient information is used.