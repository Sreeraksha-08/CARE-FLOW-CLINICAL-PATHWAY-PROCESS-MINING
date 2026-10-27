from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "process_mining" / "outputs"

# Page configuration
st.set_page_config(
    page_title="CareFlow Dashboard",
    page_icon="🏥",
    layout="wide",
)

st.title("CareFlow — Clinical Pathway Dashboard")
st.caption(
    "Process mining of simulated emergency-room patient journeys"
)

# Input files
event_file = OUTPUT_DIR / "careflow_event_log.csv"
transition_file = OUTPUT_DIR / "directly_follows_graph.csv"
process_map_file = OUTPUT_DIR / "process_map_as_is.png"

# Check required files
if not event_file.exists() or not transition_file.exists():
    st.error("Required process-mining output files are missing.")
    st.stop()

# Load data
events = pd.read_csv(event_file)
transitions = pd.read_csv(transition_file)

# Validate event columns
case_col = "case:concept:name"
activity_col = "concept:name"

if case_col not in events.columns or activity_col not in events.columns:
    st.error(
        "Expected PM4Py columns were not found. "
        f"Available columns: {', '.join(events.columns)}"
    )
    st.stop()

# KPI cards
case_count = events[case_col].nunique()
event_count = len(events)
activity_count = events[activity_col].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Patient cases", case_count)
col2.metric("Total events", event_count)
col3.metric("Distinct activities", activity_count)

st.divider()

# Process map
st.subheader("Patient pathway")

if process_map_file.exists():
    st.image(str(process_map_file), width="stretch")
else:
    st.warning("The process map PNG was not found.")

st.divider()

# Directly-follows transition chart
st.subheader("Directly-follows transitions")

if {
    "activity",
    "next_activity",
    "transition_count",
}.issubset(transitions.columns):

    fig = px.bar(
        transitions.sort_values(
            "transition_count", ascending=True
        ),
        x="transition_count",
        y="activity",
        color="next_activity",
        orientation="h",
        labels={
            "transition_count": "Transition count",
            "activity": "From activity",
            "next_activity": "To activity",
        },
        title="Number of observed transitions",
    )

    st.plotly_chart(fig, width="stretch")

else:
    st.warning(
        "Unexpected transition columns. "
        f"Available columns: {', '.join(transitions.columns)}"
    )
    st.dataframe(transitions,width="stretch")

# Data limitation
st.caption(
    "Prototype using simulated data only; "
    "not for clinical decision-making."
)