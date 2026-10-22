-- Day 11: Summarize patient pathways from simulated EHR events.

with patient_activity_summary as (

    select
        case_id,
        count(*) as total_events,
        countif(activity = 'Doctor Consultation') as doctor_consultations,
        countif(activity = 'Triage') as triage_events,
        countif(activity = 'Doctor Review') as doctor_reviews,
        countif(activity = 'X-Ray') as xray_events,
        countif(activity = 'Lab Test') as lab_events,
        min(event_timestamp) as pathway_start,
        max(event_timestamp) as pathway_end

    from {{ ref('stg_ehr_events') }}
    group by case_id

)

select
    *,
    timestamp_diff(
        pathway_end,
        pathway_start,
        minute
    ) as pathway_duration_minutes,

    case
        when doctor_consultations > 1 then true
        else false
    end as has_repeat_consultation

from patient_activity_summary