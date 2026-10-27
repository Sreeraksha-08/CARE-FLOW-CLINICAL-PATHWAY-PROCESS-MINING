SELECT
  scenario,
  loopback_reason,
  COUNT(*) AS event_count,
  COUNT(DISTINCT case_id) AS patient_count
FROM `careflow-process-mining-511911.careflow_raw.stg_ehr_events`
GROUP BY scenario, loopback_reason
ORDER BY scenario, event_count DESC;