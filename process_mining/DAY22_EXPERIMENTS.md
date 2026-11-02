# CareFlow Day 22 — Repeated Simulation Experiments

## Objective
Compare simulated before-and-after scenarios using five random seeds.

## Experiment design
- 1,000 simulated cases per run.
- Five random seeds: 42, 100, 200, 300, 400.
- Ten runs in total: five per scenario.

## Results

| Scenario | Mean loopback rate | Standard deviation | 95% CI |
|---|---:|---:|---:|
| Before | 39.82% | 2.05 | 37.27%–42.37% |
| After | 2.74% | 0.79 | 1.76%–3.72% |

## Interpretation
The mean loopback rate was 39.82% before and 2.74% after.
The difference was 37.08 percentage points.

## Limitations
- These are simulated patient journeys, not real hospital records.
- The scenarios use different configured loopback probabilities.
- Five seeds provide a limited estimate of simulation variability.
- Confidence intervals describe variation across these five runs.
- Results do not establish real-world clinical improvement.

## Validation
All ten experiment runs were checked for expected case counts and scenario labels.
