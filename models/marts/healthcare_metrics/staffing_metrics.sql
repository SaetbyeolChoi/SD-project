WITH state_hppd AS (
    SELECT
        state,
        SUM(rn_hours + lpn_hours + cna_hours) AS total_nursing_hours,
        SUM(patient_count) AS total_patient_days,
        SUM(rn_hours + lpn_hours + cna_hours) / NULLIF(SUM(patient_count), 0) AS nursing_hours_per_patient_day
    FROM {{ ref('stg_pbj_nurse_staffing') }}
    GROUP BY state
)
SELECT * FROM state_hppd