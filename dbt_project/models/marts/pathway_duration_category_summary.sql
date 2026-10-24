-- Day 13: Summarize patient pathway duration categories.

select
	pathway_duration_category,
	count(*) as patient_count,
	round(avg(pathway_duration_minutes), 2) as average_duration_minutes,
	min(pathway_duration_minutes) as minimum_duration_minutes,
	max(pathway_duration_minutes) as maximum_duration_minutes

from {{ ref('patient_pathway_duration_analysis') }}

group by pathway_duration_category

