# DAY20_GROUND_TRUTH_VALIDATION.mdDay 20 — Ground-Truth Validation

# Objective

Developed a Python evaluation module to compare the intended loopback probabilities in the CareFlow simulator configuration with the observed loopback rates in generated patient event logs.

# Implementation

- Created "process_mining/evaluate.py".
- Loaded expected loopback probabilities from "simulator/config.yaml".
- Calculated loopback cases at the patient-case level.
- Compared expected and observed rates for before and after scenarios.
- Calculated absolute error in percentage points.
- Created automated tests in "tests/test_evaluate.py".

# Validation Results

Scenario| Cases| Loopback cases| Expected rate| Observed rate| Absolute error
Before| 100| 42| 40%| 42%| 2 pp
After| 100| 4| 3%| 4%| 1 pp

The observed loopback rate decreased from 42% to 4% across the two generated samples.

# Testing

All three project tests passed, including the two new evaluator tests.

# Limitations

The results are based on simulated data and finite samples. They do not establish real-world hospital performance or clinical improvement.