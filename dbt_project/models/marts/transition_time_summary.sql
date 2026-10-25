-- Exact median for matching Python and SQL metrics.

with transition_metrics as (

    select
        activity,
        next_activity,
        transition_minutes,

        count(*) over (
            partition by activity, next_activity
        ) as transition_count,

        avg(transition_minutes) over (
            partition by activity, next_activity
        ) as average_minutes,

        percentile_cont(transition_minutes, 0.5) over (
            partition by activity, next_activity
        ) as median_minutes,

        max(transition_minutes) over (
            partition by activity, next_activity
        ) as maximum_minutes

    from {{ ref('patient_transition_times') }}

)

select distinct
    activity,
    next_activity,
    transition_count,
    round(average_minutes, 2) as average_minutes,
    round(median_minutes, 2) as median_minutes,
    maximum_minutes

from transition_metrics