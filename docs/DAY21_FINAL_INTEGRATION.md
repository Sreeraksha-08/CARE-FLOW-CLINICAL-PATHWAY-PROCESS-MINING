# Day 21 — Final Integration

## Project
CareFlow — Clinical Pathway Process Mining

## Final dataset sources
- Before: before_events_with_attributes.csv
- After: after_events_validation.csv

## Final dataset outputs
- sample_data/final/before_events_final.csv
- sample_data/final/after_events_final.csv

## Preparation
A Python script prepares consistent datasets with the same eight
columns, validates activity names and timestamps, and sorts events
by patient case and timestamp.

## Data scope
All patient journeys are simulated. No real patient data is used.

## Purpose
The final datasets are prepared for comparative process-mining
analysis and dashboard integration.