-- Day 9: Check required fields in the raw BigQuery event log.
-- A passing test returns zero rows.

select
    event_id,
    case_id,
    activity,
    event_timestamp
from `careflow-process-mining-511911.careflow_raw.raw_ehr_events`
where event_id is null
   or case_id is null
   or activity is null
   or event_timestamp is null