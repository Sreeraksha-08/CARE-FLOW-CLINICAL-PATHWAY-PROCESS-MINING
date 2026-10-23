-- Day 12: Analyze patient pathway duration.

select
    case_id,
    total_events,
    pathway_start,
    pathway_end,
    pathway_duration_minutes,
    triage_events,
    doctor_consultations,
    doctor_reviews,
    xray_events,
    lab_events,

    case
        when pathway_duration_minutes < 180 then 'Short'
        when pathway_duration_minutes <= 300 then 'Medium'
        else 'Long'
    end as pathway_duration_category

from {{ ref('patient_pathway_summary') }}