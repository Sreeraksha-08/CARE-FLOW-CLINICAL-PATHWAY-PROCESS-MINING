import random
import pandas as pd


def introduce_data_quality_issues(df, seed=42):
    """Add simulated data-quality problems to a copy of an event log."""
    rng = random.Random(seed)
    messy = df.copy()

    # 1. Duplicate approximately 2% of the events.
    duplicate_count = max(1, round(len(messy) * 0.02))
    duplicate_indices = rng.sample(
        list(messy.index),
        min(duplicate_count, len(messy))
    )
    duplicates = messy.loc[duplicate_indices].copy()
    messy = pd.concat([messy, duplicates], ignore_index=True)

    # 2. Make some activity names inconsistent.
    activity_variants = {
        "Triage": "triage",
        "Doctor Consultation": "doctor consultation",
        "X-Ray": "X-Ray ",
    }

    for original, variant in activity_variants.items():
        matching_indices = messy.index[messy["activity"] == original].tolist()
        if matching_indices:
            selected_index = rng.choice(matching_indices)
            messy.loc[selected_index, "activity"] = variant

    # 3. Make approximately 2% of timestamps missing.
    missing_count = max(1, round(len(messy) * 0.02))
    missing_indices = rng.sample(
        list(messy.index),
        min(missing_count, len(messy))
    )
    messy.loc[missing_indices, "timestamp"] = pd.NaT

    return messy


if __name__ == "__main__":
    input_path = "sample_data/before_events.csv"
    output_path = "sample_data/day5_messy_events.csv"

    events = pd.read_csv(input_path, parse_dates=["timestamp"])
    messy_events = introduce_data_quality_issues(events)

    messy_events.to_csv(output_path, index=False)

    print("Data-quality simulation completed.")
    print(f"Original events: {len(events)}")
    print(f"Events after duplicates: {len(messy_events)}")
    print(
        "Missing timestamps:",
        messy_events["timestamp"].isna().sum()
    )
    print("\nActivity names:")
    print(messy_events["activity"].value_counts().to_string())
    print(f"\nSaved to: {output_path}")