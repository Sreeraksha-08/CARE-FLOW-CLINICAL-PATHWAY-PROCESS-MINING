# CareFlow — Simulation Assumptions

## 1. Purpose

CareFlow uses simulated emergency-room patient journeys to demonstrate data engineering, process mining and healthcare operations analytics.

## 2. Patient Cases

The current comparison uses 100 simulated patient cases in each scenario.

Each case represents one simulated patient journey.

## 3. Clinical Activities

The simulated workflow includes:

- Registration
- Triage
- Doctor Consultation
- X-Ray
- Lab Test
- Doctor Review
- Discharge

## 4. Repeated Activities

Repeated Triage events are included in the simulation to represent pathway loopbacks.

The before-and-after comparison measures how frequently these repeated activities occur.

## 5. Scenario Comparison

The before and after datasets are generated under different simulation assumptions.

Their differences demonstrate how process-mining analysis can compare two simulated workflows.

## 6. Duration Measures

Pathway duration is calculated from the first to the last event timestamp for each patient case.

The reported average is based on the simulated cases in each scenario.

## 7. Interpretation

A lower simulated loopback rate or pathway duration does not prove that a real hospital workflow has improved.

The results are illustrative and depend on the simulator's configuration.

## 8. Limitations

- No real patient records are used.
- No clinical outcomes are modelled.
- Simulation assumptions may not reflect actual hospital operations.
- The analysis is not a controlled clinical study.

## 9. Intended Use

The project is intended for educational demonstration of process mining and healthcare operations analytics. It is not intended for clinical decision-making.