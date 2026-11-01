# CareFlow — Day 21 Release Notes

## Project Overview

CareFlow is a simulated clinical pathway process-mining prototype. It combines data engineering, data transformation, process discovery, analytical comparison and dashboard visualisation.

## Day 21 Development

- Prepared consistent final before-and-after simulated event datasets.
- Added Python-based scenario comparison analysis.
- Generated scenario and activity comparison CSV outputs.
- Integrated before-and-after comparisons into the Streamlit dashboard.
- Updated project documentation and README.

## Scenario Comparison

Metric| Before| After
Patient cases| 100| 100
Event records| 668| 626
Patients with repeated Triage| 42| 4
Loopback rate| 42%| 4%
Average pathway duration| 264.70 min| 240.74 min

## Main Technologies

- Python and pandas
- Google BigQuery and SQL
- dbt
- PM4Py
- Streamlit
- Power BI
- Git and GitHub

## Important Limitations

All patient journeys are simulated. The before-and-after results are based on the simulation assumptions and do not establish actual hospital performance or clinical improvement.

CareFlow is an educational analytics prototype, not a deployed clinical system.