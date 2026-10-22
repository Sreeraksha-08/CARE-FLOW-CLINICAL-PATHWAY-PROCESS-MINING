-- Day 11: Every patient pathway must contain at least one event.

select
	case_id,
	total_events
from {{ ref('patient_pathway_summary') }}
where total_events <= 0
   or total_events is null
