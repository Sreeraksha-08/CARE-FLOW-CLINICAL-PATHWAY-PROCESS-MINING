# CareFlow — Clinical Pathway Process Mining

## Project Overview

CareFlow is a data-driven process-mining project that analyses simulated emergency-room patient journeys.

The project uses Python to generate patient event logs, Google BigQuery to store event data, dbt to transform and validate the data, PM4Py to discover patient pathways, and Power BI and Streamlit to visualise analytical results.

The objective is to understand how simulated patients move through clinical activities, identify repeated activities, compare pathway variations, and investigate potential workflow bottlenecks.

This project uses simulated data only. It is not a deployed clinical system and does not represent actual hospital performance.

## Project Objectives

- Generate simulated emergency-room patient journeys.
- Store and query event data using Google BigQuery.
- Transform and validate data using dbt.
- Discover patient pathways using process mining.
- Analyse activity transitions and pathway durations.
- Compare simulated before-and-after scenarios.
- Visualise findings through interactive dashboards.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Event generation and data analysis |
| Google BigQuery | Cloud data warehouse |
| SQL | Data querying and analysis |
| dbt | Data transformation and testing |
| PM4Py | Process discovery and mining |
| Streamlit | Interactive dashboard |
| Power BI | Business intelligence visualisation |
| Git and GitHub | Version control and collaboration |

## Project Architecture

1. Simulation: Python generates simulated emergency-room event logs.
2. Data warehouse: Event data is loaded into BigQuery.
3. Transformation: dbt creates staging and analytical models.
4. Validation: Data-quality tests check event records.
5. Process mining: PM4Py discovers directly-follows relationships and process maps.
6. Analysis: Python and SQL analyse pathway durations, transitions, and repeated activities.
7. Visualisation: Streamlit and Power BI present the analytical findings.

## Repository Structure

```text
CARE-FLOW-CLINICAL-PATHWAY-PROCESS-MINING/
├── analysis/
│   ├── bottleneck_analysis.py
│   ├── prepare_final_datasets.py
│   ├── compare_final_scenarios.py
│   └── final_outputs/
├── dashboard/
│   ├── app.py
│   └── CareFlow_Dashboard.pbix
├── dbt_project/
│   ├── models/
│   └── DAY9_TESTING.md
├── docs/
│   ├── setup.md
│   ├── work_plan.md
│   ├── DAY21_FINAL_INTEGRATION.md
│   └── DAY21_DASHBOARD_INTEGRATION.md
├── process_mining/
│   ├── discover_process.py
│   ├── evaluate.py
│   └── outputs/
├── sample_data/
│   └── final/
├── simulator/
│   ├── generate_events.py
│   ├── attributes.py
│   ├── config.yaml
│   └── data_quality.py
├── tests/
├── warehouse/
│   ├── schema.py
│   └── load_to_bigquery.py
└── README.md
```

## Simulated Dataset

The final comparison uses two simulated datasets.

| Metric | Before | After |
|---|---:|---:|
| Patient cases | 100 | 100 |
| Event records | 668 | 626 |
| Patients with repeated Triage | 42 | 4 |
| Loopback rate | 42% | 4% |
| Average pathway duration | 264.70 min | 240.74 min |

The simulation includes activities such as:

- Registration
- Triage
- Doctor Consultation
- X-Ray
- Lab Test
- Doctor Review
- Discharge

## Process Mining Findings

The discovered process map identifies variations in the simulated patient pathways.

The before scenario contains 42 patients with repeated Triage activities, compared with 4 in the after scenario.

The results demonstrate how process mining can identify repeated activities and pathway variations in simulated workflows.

## Dashboard

The Streamlit dashboard includes:

- Patient case count
- Total event count
- Distinct activity count
- Patient pathway process map
- Directly-follows transition chart
- Before-and-after loopback comparison
- Average pathway duration comparison
- Activity volume comparison

A Power BI dashboard is also included for additional visual analysis.

## Running the Project


### 1. Clone the repository

```powershell
git clone https://github.com/Sreeraksha-08/CARE-FLOW-CLINICAL-PATHWAY-PROCESS-MINING.git
```

### 2. Open the project directory

```powershell
cd CARE-FLOW-CLINICAL-PATHWAY-PROCESS-MINING
```

### 3. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Generate simulated events

```powershell
python .\simulator\generate_events.py --scenario before --cases 100 --output sample_data\before_events.csv
```

### 6. Discover the process

```powershell
python .\process_mining\discover_process.py
```

### 7. Prepare final datasets

```powershell
python .\analysis\prepare_final_datasets.py
```

### 8. Compare scenarios

```powershell
python .\analysis\compare_final_scenarios.py
```

### 9. Run the Streamlit dashboard

```powershell
python -m streamlit run .\dashboard\app.py
```

Note: BigQuery and dbt workflows require their respective configuration and credentials. Follow "docs/setup.md" before running warehouse operations.

## Limitations

- Patient journeys are simulated, not collected from real hospitals.
- Results depend on the simulation configuration and assumptions.
- The before-and-after comparison is not a controlled clinical study.
- Identified repeated activities are potential workflow investigation points, not proof of actual clinical bottlenecks.
- The project is an educational analytics prototype, not a clinical decision-support system.

## Future Improvements

- Explore additional patient pathway variations.
- Develop more realistic simulation scenarios.
- Improve dashboard interactivity.
- Investigate predictive process monitoring.

## Project Status

Development: Initial prototype and Day 21 integration work.

Data: Simulated emergency-room patient event logs.

Purpose: Demonstrates data engineering, SQL, process mining, and visual analytics.