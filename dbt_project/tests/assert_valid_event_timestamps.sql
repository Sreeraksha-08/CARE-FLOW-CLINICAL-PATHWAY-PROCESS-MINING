-- Day 9: Check for missing event timestamps.
-- A passing test returns zero rows.

select
    event_id,
    case_id,
    event_timestamp
from {{ ref('stg_ehr_events') }}
where event_timestamp is null