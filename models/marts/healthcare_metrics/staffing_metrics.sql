WITH nurse_hours AS (
    SELECT
        hospital_id,
        state,
        month,
        SUM(rn_hours + lpn_hours + cna_hours) AS total_nurse_hours
    FROM {{ ref('stg_pbj_nurse_staffing') }}
    GROUP BY hospital_id, state, month
)
SELECT * FROM nurse_hours