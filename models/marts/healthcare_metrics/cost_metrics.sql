WITH payroll_estimate AS (
    SELECT
        hospital_id,
        state,
        SUM(rn_hours + lpn_hours + cna_hours) * 35 AS estimated_payroll
    FROM {{ ref('stg_pbj_nurse_staffing') }}
    GROUP BY hospital_id, state
)
SELECT * FROM payroll_estimate
