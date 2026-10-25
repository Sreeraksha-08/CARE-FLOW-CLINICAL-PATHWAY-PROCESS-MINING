-- Day 14: Calculate time between consecutive patient activities.

with ordered_events as (

    select
        case_id,
        activity,
        event_timestamp,

        lead(activity) over (
            partition by case_id
            order by event_timestamp
        ) as next_activity,

        lead(event_timestamp) over (
            partition by case_id
            order by event_timestamp
        ) as next_event_timestamp

    from {{ ref('stg_ehr_events') }}

),

transition_times as (

    select
        case_id,
        activity,
        next_activity,
        event_timestamp,
        next_event_timestamp,

        timestamp_diff(
            next_event_timestamp,
            event_timestamp,
            minute
        ) as transition_minutes

    from ordered_events
    where next_event_timestamp is not null

)

select *
from transition_times