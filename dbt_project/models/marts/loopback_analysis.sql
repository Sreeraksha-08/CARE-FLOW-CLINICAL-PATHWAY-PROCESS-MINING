-- Summarize simulated patient loopbacks by scenario and reason.

select
    scenario,
    loopback_reason,
    count(*) as event_count,
    count(distinct case_id) as patient_count
from {{ ref('stg_ehr_events') }}
where loopback_reason is not null
group by
    scenario,
    loopback_reason
