from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "process_mining" / "outputs"
FINAL_OUTPUT_DIR = PROJECT_ROOT / "analysis" / "final_outputs"


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CareFlow Dashboard",
    page_icon="🏥",
    layout="wide",
)

st.title("CareFlow — Clinical Pathway Dashboard")
st.caption(
    "Process mining of simulated emergency-room patient journeys"
)


# --------------------------------------------------
# INPUT FILES
# --------------------------------------------------

event_file = OUTPUT_DIR / "careflow_event_log.csv"
transition_file = OUTPUT_DIR / "directly_follows_graph.csv"
process_map_file = OUTPUT_DIR / "process_map_as_is.png"

scenario_file = FINAL_OUTPUT_DIR / "scenario_comparison.csv"
activity_file = FINAL_OUTPUT_DIR / "activity_comparison.csv"


# --------------------------------------------------
# LOAD PROCESS-MINING DATA
# --------------------------------------------------

if not event_file.exists() or not transition_file.exists():
    st.error("Required process-mining output files are missing.")
    st.stop()

events = pd.read_csv(event_file)
transitions = pd.read_csv(transition_file)


# --------------------------------------------------
# VALIDATE EVENT COLUMNS
# --------------------------------------------------

case_col = "case:concept:name"
activity_col = "concept:name"

if case_col not in events.columns or activity_col not in events.columns:
    st.error(
        "Expected PM4Py columns were not found. "
        f"Available columns: {', '.join(events.columns)}"
    )
    st.stop()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

case_count = events[case_col].nunique()
event_count = len(events)
activity_count = events[activity_col].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Patient cases", case_count)
col2.metric("Total events", event_count)
col3.metric("Distinct activities", activity_count)

st.divider()


# --------------------------------------------------
# PROCESS MAP
# --------------------------------------------------

st.subheader("Patient pathway")

if process_map_file.exists():
    st.image(str(process_map_file), width="stretch")
else:
    st.warning("The process map PNG was not found.")

st.divider()


# --------------------------------------------------
# DIRECTLY-FOLLOWS TRANSITION CHART
# --------------------------------------------------

st.subheader("Directly-follows transitions")

if {
    "activity",
    "next_activity",
    "transition_count",
}.issubset(transitions.columns):

    fig = px.bar(
        transitions.sort_values(
            "transition_count",
            ascending=True,
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
    st.dataframe(transitions, width="stretch")


# --------------------------------------------------
# DAY 21: BEFORE-AND-AFTER SCENARIO COMPARISON
# --------------------------------------------------

st.divider()
st.header("Before-and-After Scenario Comparison")

if scenario_file.exists() and activity_file.exists():

    scenario_data = pd.read_csv(scenario_file)
    activity_data = pd.read_csv(activity_file)

    required_scenario_columns = {
        "scenario",
        "loopback_rate_percent",
        "average_pathway_duration_minutes",
    }

    if not required_scenario_columns.issubset(scenario_data.columns):
        st.error("Scenario comparison file has unexpected columns.")
        st.stop()

    if "activity" not in activity_data.columns:
        st.error("Activity comparison file has no activity column.")
        st.stop()

    before_rows = scenario_data.loc[
        scenario_data["scenario"] == "before"
    ]

    after_rows = scenario_data.loc[
        scenario_data["scenario"] == "after"
    ]

    if before_rows.empty or after_rows.empty:
        st.error("Before or after scenario data is missing.")
        st.stop()

    before = before_rows.iloc[0]
    after = after_rows.iloc[0]

    st.subheader("Patient Pathway Outcomes")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Before Loopback Rate",
        f"{before['loopback_rate_percent']:.1f}%",
    )

    col2.metric(
        "After Loopback Rate",
        f"{after['loopback_rate_percent']:.1f}%",
        delta=(
            f"{after['loopback_rate_percent'] - before['loopback_rate_percent']:.1f}"
            " percentage points"
        ),
        delta_color="inverse",
    )

    col3.metric(
        "Average Duration After",
        f"{after['average_pathway_duration_minutes']:.1f} min",
        delta=(
            f"{after['average_pathway_duration_minutes'] - before['average_pathway_duration_minutes']:.1f}"
            " min"
        ),
        delta_color="inverse",
    )

    # Average pathway duration chart
    st.subheader("Average Pathway Duration")

    duration_chart = px.bar(
        scenario_data,
        x="scenario",
        y="average_pathway_duration_minutes",
        color="scenario",
        labels={
            "scenario": "Scenario",
            "average_pathway_duration_minutes": "Average Duration (minutes)",
        },
        title="Average Patient Pathway Duration",
    )

    st.plotly_chart(duration_chart, width="stretch")

    # Activity volume comparison
    st.subheader("Activity Volume Comparison")

    activity_chart_data = activity_data.melt(
        id_vars="activity",
        var_name="scenario",
        value_name="event_count",
    )

    activity_chart = px.bar(
        activity_chart_data,
        x="activity",
        y="event_count",
        color="scenario",
        barmode="group",
        labels={
            "activity": "Clinical Activity",
            "event_count": "Number of Events",
            "scenario": "Scenario",
        },
        title="Activity Counts: Before vs After",
    )

    st.plotly_chart(activity_chart, width="stretch")

    st.caption(
        "All comparisons use simulated patient journeys. "
        "They do not establish real-world clinical improvement."
    )

else:
    st.warning(
        "Scenario comparison files are not available. "
        "Run analysis/compare_final_scenarios.py first."
    )


# --------------------------------------------------
# DATA LIMITATION
# --------------------------------------------------

st.divider()

st.caption(
    "CareFlow is a prototype using simulated data only. "
    "It is not intended for clinical decision-making."
)