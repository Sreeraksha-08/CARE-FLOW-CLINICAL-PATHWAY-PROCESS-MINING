# CareFlow — Command Reference

Run these commands from the project root in Windows PowerShell.

# 1. Activate the virtual environment

.\.venv\Scripts\Activate.ps1

# 2. Install Python dependencies

pip install -r requirements.txt

# 3. Generate simulated patient events

python .\simulator\generate_events.py --scenario before --cases 100 --output sample_data\before_events.csv

# 4. Prepare final datasets

python .\analysis\prepare_final_datasets.py

# 5. Discover patient pathways

python .\process_mining\discover_process.py

# 6. Compare before-and-after scenarios

python .\analysis\compare_final_scenarios.py

# 7. Run automated tests

python -m pytest

# 8. Launch the Streamlit dashboard

python -m streamlit run .\dashboard\app.py

## Important Notes

- Run commands from the repository root unless otherwise stated.
- These commands operate on simulated data.
- BigQuery and dbt commands require their own configuration and credentials.
- Check the project setup documentation before running warehouse operations.