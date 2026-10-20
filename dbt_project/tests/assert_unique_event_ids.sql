-- Day 9: Check for duplicate event IDs.
-- A passing test returns zero rows.

select
	event_id
from {{ ref('stg_ehr_events') }}
group by event_id
having count(*) > 1
