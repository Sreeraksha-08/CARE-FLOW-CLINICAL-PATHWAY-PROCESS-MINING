# CareFlow — Project Handover

## 1. Project Overview

CareFlow is a simulated clinical pathway process-mining and healthcare operations analytics prototype.

It analyses simulated emergency-room patient journeys to understand clinical activity sequences, repeated activities and pathway variations.

## 2. Main Technologies

- Python and pandas
- Google BigQuery
- SQL
- dbt
- PM4Py
- Streamlit
- Power BI
- Git and GitHub

## 3. Main Project Components

Component| Responsibility
Simulator| Generates simulated patient event logs
Warehouse| Stores event data in BigQuery
dbt| Transforms and validates event data
Process mining| Discovers patient pathways
Analysis| Compares activity transitions and durations
Streamlit| Displays interactive analytical results
Power BI| Provides business intelligence visualisation

## 4. Final Scenario Comparison

Metric| Before| After
Patient cases| 100| 100
Event records| 668| 626
Repeated Triage cases| 42| 4
Loopback rate| 42%| 4%
Average pathway duration| 264.70 min| 240.74 min

## 5. Important Output Files

- "sample_data/final/before_events_final.csv"
- "sample_data/final/after_events_final.csv"
- "analysis/final_outputs/scenario_comparison.csv"
- "analysis/final_outputs/activity_comparison.csv"
- "process_mining/outputs/process_map_as_is.png"

## 6. Running the Dashboard

From the project root, activate the virtual environment and run:

python -m streamlit run .\dashboard\app.py

## 7. Data Privacy and Limitations

- All patient journeys are simulated.
- No real patient records are used.
- Results depend on the simulation assumptions.
- The comparison does not establish actual hospital performance.
- CareFlow is not a deployed clinical or decision-support system.

## 8. Future Development

- Improve bottleneck analysis.
- Explore additional pathway variations.
- Improve dashboard interactivity.
- Investigate predictive process monitoring.

## 9. Handover Status

CareFlow contains a simulated-data analytics workflow covering event generation, data warehousing, transformation, process mining, scenario comparison and visualisation.

Final repository inspection and GitHub release approval remain separate activities.