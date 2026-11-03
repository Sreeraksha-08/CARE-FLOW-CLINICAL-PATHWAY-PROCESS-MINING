# CareFlow — Day 23 Sensitivity Analysis

## Objective
Study how configured loopback probabilities affect observed loopback rates in simulated emergency-room journeys.

## Methodology
- Simulated cases per experiment: 1000
- Configured probabilities: 10%, 20%, 30%, 40%, 50%
- Random seeds: 42, 100, 200, 300, 400
- Total experiments: 25
- Each probability uses five independent seed-level runs.

## Statistical summary
|   configured_probability_percent |   mean_observed_rate_percent |   standard_deviation |   ci_95_lower |   ci_95_upper |
|---------------------------------:|-----------------------------:|---------------------:|--------------:|--------------:|
|                               10 |                         9.62 |             0.496991 |        9.0029 |       10.2371 |
|                               20 |                        19.96 |             1.11714  |       18.5729 |       21.3471 |
|                               30 |                        29.38 |             1.12561  |       27.9824 |       30.7776 |
|                               40 |                        39.82 |             2.05353  |       37.2702 |       42.3698 |
|                               50 |                        49.82 |             1.31605  |       48.1859 |       51.4541 |

The confidence intervals are t-based 95% intervals across five seed-level observed rates per probability.

## Interpretation
Observed rates may differ from configured probabilities because each simulation uses a finite number of cases.
The experiment measures simulator behaviour, not real hospital performance.

## Outputs
- sensitivity_results.csv
- sensitivity_summary.csv
- sensitivity_analysis.png
- 25 experiment event-log CSV files

## Validation
All 25 experiments, case counts and loopback rates were checked by the script.