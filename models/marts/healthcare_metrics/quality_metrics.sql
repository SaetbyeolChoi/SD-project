WITH readmission_rates AS (
    SELECT
        hospital_id,
        state,
        diagnosis_category,
        readmission_rate
    FROM {{ ref('stg_quality_measures') }}
)
SELECT * FROM readmission_rates