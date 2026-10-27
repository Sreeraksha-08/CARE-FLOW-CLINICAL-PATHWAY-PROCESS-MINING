-- Summarize simulated patient events by scenario and loopback reason.

select
    scenario,
    loopback_reason,
    count(*) as event_count,
    count(distinct case_id) as patient_count
from {{ ref('stg_ehr_events') }}
group by
    scenario,
    loopback_reason