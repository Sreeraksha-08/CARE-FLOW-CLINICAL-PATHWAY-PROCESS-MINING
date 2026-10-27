SELECT
  scenario,
  loopback_reason,
  event_count,
  patient_count
FROM `careflow-process-mining-511911.careflow_raw.loopback_analysis`
ORDER BY scenario, event_count DESC;
