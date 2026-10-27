"""Discover the simulated CareFlow process using PM4Py."""

from pathlib import Path

import pandas as pd
import pm4py
import matplotlib.pyplot as plt


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = (
    PROJECT_ROOT
    / "sample_data"
    / "before_events_with_attributes_recent.csv"
)
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load and validate the simulated event data
    df = pd.read_csv(INPUT_FILE)

    required_columns = {"case_id", "activity", "timestamp"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")

    if df[["case_id", "activity", "timestamp"]].isna().any().any():
        raise ValueError("Case ID, activity, and timestamp must not be missing.")

    df = df.sort_values(["case_id", "timestamp"]).copy()

    # Convert the data into PM4Py's event-log format
    event_log = pm4py.format_dataframe(
        df,
        case_id="case_id",
        activity_key="activity",
        timestamp_key="timestamp",
    )

    log_path = OUTPUT_DIR / "careflow_event_log.csv"
    event_log.to_csv(log_path, index=False)

    # Discover the directly-follows graph
    dfg, start_activities, end_activities = (
        pm4py.discover_dfg(event_log)
    )

    # Save transition counts for analysis
    transition_rows = [
        {
            "activity": source,
            "next_activity": target,
            "transition_count": count,
        }
        for (source, target), count in dfg.items()
    ]

    transitions = pd.DataFrame(
        transition_rows,
        columns=["activity", "next_activity", "transition_count"],
    )

    transitions = transitions.sort_values(
        "transition_count", ascending=False
    )

    transitions_path = OUTPUT_DIR / "directly_follows_graph.csv"
    transitions.to_csv(transitions_path, index=False)
    process_map_path = OUTPUT_DIR / "process_map_as_is.png"
    create_process_map(transitions, process_map_path)

    # Save start and end activity counts
    summary = {
        "start_activities": start_activities,
        "end_activities": end_activities,
    }
    summary_path = OUTPUT_DIR / "process_summary.txt"

    with summary_path.open("w", encoding="utf-8") as file:
        file.write(f"Cases: {df['case_id'].nunique()}\n")
        file.write(f"Events: {len(df)}\n")
        file.write(f"Start activities: {start_activities}\n")
        file.write(f"End activities: {end_activities}\n")

    print(f"Cases: {df['case_id'].nunique()}")
    print(f"Events: {len(df)}")
    print(f"Distinct activities: {df['activity'].nunique()}")
    print(f"Directly-follows transitions: {len(dfg)}")
    print(f"Event log saved: {log_path}")
    print(f"Transition counts saved: {transitions_path}")
    print(f"Process summary saved: {summary_path}")

def create_process_map(transitions, output_path):
    """Draw the discovered CareFlow process and save it as a PNG."""
    from matplotlib.patches import FancyBboxPatch

    positions = {
        "Registration": (0, 2),
        "Triage": (2, 2),
        "Doctor Consultation": (4.5, 2.8),
        "Lab Test": (6.5, 0.5),
        "X-Ray": (6.5, 2.8),
        "Doctor Review": (9, 2),
        "Discharge": (11, 2),
    }

    fig, ax = plt.subplots(figsize=(16, 7))
    ax.set_title("CareFlow — Simulated Emergency Room Process Map", fontsize=16)
    ax.axis("off")

    # Draw transitions and label them with their observed counts.
    for _, row in transitions.iterrows():
        source = row["activity"]
        target = row["next_activity"]
        count = int(row["transition_count"])

        x1, y1 = positions[source]
        x2, y2 = positions[target]

        # Curve the two returning/alternate paths to reduce overlap.
        curve = 0
        if (source, target) == ("X-Ray", "Triage"):
            curve = 0.35
        elif (source, target) == ("Triage", "Doctor Review"):
            curve = -0.25
        elif (source, target) == ("Doctor Consultation", "Lab Test"):
            curve = 0.12

        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops={
                "arrowstyle": "->",
                "connectionstyle": f"arc3,rad={curve}",
                "linewidth": 1.5,
                "color": "black",
                "shrinkA": 35,
                "shrinkB": 35,
            },
        )

        label_x = (x1 + x2) / 2
        label_y = (y1 + y2) / 2 + (0.25 if curve >= 0 else -0.25)
        ax.text(
            label_x,
            label_y,
            str(count),
            ha="center",
            va="center",
            fontsize=10,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 2},
        )

    # Draw one labelled box for each activity.
    for activity, (x, y) in positions.items():
        box = FancyBboxPatch(
            (x - 0.65, y - 0.28),
            1.3,
            0.56,
            boxstyle="round,pad=0.08",
            facecolor="white",
            edgecolor="black",
            linewidth=1.5,
        )
        ax.add_patch(box)
        ax.text(x, y, activity, ha="center", va="center", fontsize=9)

    ax.text(
        5.5,
        -0.25,
        "Arrow labels = observed transition counts",
        ha="center",
        fontsize=10,
    )
    ax.set_xlim(-1, 12)
    ax.set_ylim(-0.7, 4)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
if __name__ == "__main__":
    main()