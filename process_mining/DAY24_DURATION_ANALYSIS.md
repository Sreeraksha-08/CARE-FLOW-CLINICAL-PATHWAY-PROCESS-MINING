# CareFlow — Day 24: Duration Analysis

## Objective
Analyse simulated activity intervals and total patient pathway durations.

## Methodology
- Events are sorted by case ID and timestamp.
- Activity interval duration is calculated as the time until the next event in the same case.
- The final event in each case has no subsequent interval and is excluded from activity-level duration statistics.
- Patient pathway duration is calculated from the first to the last event.
- Mean, median, minimum and maximum pathway durations are compared.

## Patient pathway comparison
| scenario   |   cases |   mean_minutes |   median_minutes |   max_minutes |   min_minutes |
|:-----------|--------:|---------------:|-----------------:|--------------:|--------------:|
| after      |     100 |         240.74 |              242 |           349 |            91 |
| before     |     100 |         264.7  |              267 |           437 |           166 |

## Activity duration summary
| scenario   | activity            |   event_intervals |   mean_minutes |   median_minutes |   max_minutes |
|:-----------|:--------------------|------------------:|---------------:|-----------------:|--------------:|
| before     | Doctor Consultation |               100 |        46.31   |             45   |            89 |
| before     | Doctor Review       |               100 |        48.92   |             50   |            90 |
| before     | Lab Test            |                26 |        50.1154 |             58   |            84 |
| before     | Registration        |               100 |        47.87   |             45   |            89 |
| before     | Triage              |               142 |        47.0493 |             47.5 |            90 |
| before     | X-Ray               |               100 |        41.76   |             39.5 |            89 |
| after      | Doctor Consultation |               100 |        47.54   |             45   |            90 |
| after      | Doctor Review       |               100 |        43.81   |             42   |            89 |
| after      | Lab Test            |                22 |        40.6818 |             39.5 |            90 |
| after      | Registration        |               100 |        46.08   |             47   |            88 |
| after      | Triage              |               104 |        43.9712 |             39.5 |            90 |
| after      | X-Ray               |               100 |        48.63   |             46.5 |            89 |

## Interpretation
Activity intervals represent elapsed time between consecutive recorded events. They do not necessarily represent the exact time spent performing an activity.
Long intervals may indicate periods worth investigating, but do not independently prove a clinical bottleneck.

## Limitations
All data is simulated. Before-and-after differences reflect the simulated scenarios and must not be interpreted as real hospital improvements.

## Generated outputs
- activity_duration_summary.csv
- patient_pathway_duration.csv
- scenario_comparison.csv
- activity_scenario_comparison.csv
- activity_duration.png
- pathway_comparison.png

## Validation
Both scenarios, patient counts, duration values and output files were checked.