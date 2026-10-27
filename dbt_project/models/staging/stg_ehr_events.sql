-- Stage the simulated CareFlow healthcare event log.
-- The raw BigQuery table is not modified.

select
    cast(event_id as string) as event_id,
    cast(case_id as string) as case_id,
    trim(cast(activity as string)) as activity,
    cast(event_timestamp as timestamp) as event_timestamp,
    cast(resource as string) as resource,
    cast(department as string) as department,
    cast(age_group as string) as age_group,
    cast(loopback_reason as string) as loopback_reason,
    cast(scenario as string) as scenario
from `careflow-process-mining-511911.careflow_raw.raw_ehr_events`
where event_id is not null
  and case_id is not null
  and activity is not null
  and event_timestamp is not null
