# CareFlow — Technical Workflow

## 1. Event Generation

The Python simulator generates synthetic emergency-room patient journeys.

Each event contains information such as:

- Patient case ID
- Clinical activity
- Event timestamp
- Resource
- Department
- Age group
- Scenario information

## 2. Data Warehousing

Google BigQuery stores the simulated event records in the raw event table.

The warehouse provides a central location for querying and analysing event data.

## 3. Data Transformation

dbt transforms raw event records into staging and analytical models using SQL.

## 4. Data Validation

Data-quality tests check important properties such as:

- Required event fields
- Unique event identifiers
- Valid timestamps
- Positive patient pathway event counts

## 5. Process Mining

PM4Py analyses event sequences and discovers directly-follows relationships between clinical activities.

The process map represents the observed pathways in the simulated event log.

## 6. Analytical Comparison

Python and pandas compare the before-and-after datasets.

The analysis includes:

- Patient case counts
- Event counts
- Repeated Triage cases
- Loopback rates
- Average pathway duration
- Activity volume

## 7. Dashboard Visualisation

Streamlit presents process maps, transition charts and scenario comparisons.

Power BI provides additional business intelligence visualisation.

## 8. Data Flow Summary

Python Simulator → BigQuery → dbt → Process Mining → Python Analysis → Streamlit and Power BI

## 9. Scope

This workflow demonstrates an analytical approach using simulated data. It does not establish real clinical outcomes or hospital performance.