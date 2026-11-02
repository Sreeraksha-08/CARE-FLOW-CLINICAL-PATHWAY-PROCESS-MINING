"""Complete the final three Day 22 tasks."""

from pathlib import Path
import math
import statistics
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "process_mining" / "experiments"
RESULTS = FOLDER / "experiment_results.csv"
DOC = ROOT / "process_mining" / "DAY22_EXPERIMENTS.md"

# Read experiment results
df = pd.read_csv(RESULTS)

# Validate experiment structure
assert len(df) == 10, "Expected 10 experiment runs"
assert df["seed"].nunique() == 5, "Expected 5 random seeds"
assert set(df["scenario"]) == {"before", "after"}
assert (df["cases"] == 1000).all()

# Calculate mean and 95% confidence intervals
# t critical value for 5 observations and 4 degrees of freedom
t_critical = 2.776445

summary = []

for scenario in ["before", "after"]:
    values = df.loc[
        df["scenario"] == scenario,
        "loopback_rate_percent"
    ].tolist()

    mean = statistics.mean(values)
    sd = statistics.stdev(values)
    margin = t_critical * sd / math.sqrt(len(values))

    summary.append({
        "scenario": scenario,
        "mean": mean,
        "sd": sd,
        "lower": mean - margin,
        "upper": mean + margin,
    })

# Create documentation
lines = [
    "# CareFlow Day 22 — Repeated Simulation Experiments",
    "",
    "## Objective",
    "Compare simulated before-and-after scenarios using five random seeds.",
    "",
    "## Experiment design",
    "- 1,000 simulated cases per run.",
    "- Five random seeds: 42, 100, 200, 300, 400.",
    "- Ten runs in total: five per scenario.",
    "",
    "## Results",
    "",
    "| Scenario | Mean loopback rate | Standard deviation | 95% CI |",
    "|---|---:|---:|---:|",
]

for item in summary:
    lines.append(
        f"| {item['scenario'].title()} "
        f"| {item['mean']:.2f}% "
        f"| {item['sd']:.2f} "
        f"| {item['lower']:.2f}%–{item['upper']:.2f}% |"
    )

before = next(x for x in summary if x["scenario"] == "before")
after = next(x for x in summary if x["scenario"] == "after")

lines += [
    "",
    "## Interpretation",
    f"The mean loopback rate was {before['mean']:.2f}% "
    f"before and {after['mean']:.2f}% after.",
    f"The difference was {before['mean'] - after['mean']:.2f} "
    "percentage points.",
    "",
    "## Limitations",
    "- These are simulated patient journeys, not real hospital records.",
    "- The scenarios use different configured loopback probabilities.",
    "- Five seeds provide a limited estimate of simulation variability.",
    "- Confidence intervals describe variation across these five runs.",
    "- Results do not establish real-world clinical improvement.",
    "",
    "## Validation",
    "All ten experiment runs were checked for expected case counts "
    "and scenario labels.",
]

DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")

# Validate all ten generated datasets
for seed in [42, 100, 200, 300, 400]:
    for scenario in ["before", "after"]:
        path = FOLDER / f"{scenario}_seed_{seed}.csv"
        assert path.exists(), f"Missing file: {path}"

print("\n95% CONFIDENCE INTERVALS")
print(pd.DataFrame(summary).to_string(index=False))

print("\nFINAL VALIDATION")
print("Experiment rows:", len(df))
print("Random seeds:", df["seed"].nunique())
print("Cases per run: 1,000")
print("Generated datasets: 10")
print("Documentation:", DOC)
print("All final checks passed!")
