# CareFlow — Day 9: Data Quality Testing

## Objective

Validate the simulated healthcare event log using dbt data tests.

## Tests Implemented

1. Raw event field validation — checks for missing event IDs, case IDs, activity names, and timestamps in the raw BigQuery table.
2. Unique event IDs — checks for duplicate event IDs in the staged event model.
3. Valid timestamps — checks for missing timestamps in the staged event model.

## Results

- Tests passed: 3
- Warnings: 0
- Errors: 0

All three tests completed successfully.

## Why Testing Matters

Reliable event data is necessary for accurate process discovery, activity ordering, waiting-time calculations, bottleneck identification, and dashboard reporting.

## Data Privacy

Development uses simulated healthcare data. No real patient information or credentials should be committed to the repository.

## Next Step

Continue improving the data-quality checks before proceeding to process-mining analysis.