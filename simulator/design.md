# CareFlow Simulator Design

## Purpose

Generate simulated Emergency Room (ER) event logs for process mining. All records must be synthetic and must not represent real patients.

## Normal patient journey

Each case follows this sequence:

1. Registration
2. Triage
3. Doctor Consultation
4. X-Ray
5. Doctor Review
6. Discharge

Approximately 30% of cases include a `Lab Test` after `Doctor Consultation` and before `X-Ray`.

## Scenarios

### Before improvement

Approximately 40% of cases loop back after `X-Ray`: return to `Triage`, repeat `X-Ray`, then continue to `Doctor Review`. Assign one of these reasons to each loop:

- `missing_paperwork_form`
- `insurance_info_missing`
- `wrong_department`

### After improvement

The improved intake form reduces the loop-back rate to approximately 3%. The loop sequence and possible reasons remain unchanged.

## Event log and data quality

Record each activity as an event associated with a unique synthetic case identifier and a timestamp when available. Simulated data may contain duplicate events, inconsistent activity names, and missing timestamps. These quality issues should be representable in generated logs for process-mining tests.

## Reproducibility

Accept a random seed and use it for all randomized choices. The same seed and configuration must reproduce the same event log.

## Data safety

Generate simulated data only. Do not use real patient records or personally identifiable information.
