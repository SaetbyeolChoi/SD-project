WITH source AS (
    SELECT
        CCN AS hospital_id,
        State AS state,
        Measure_Description AS diagnosis_category,
        Adjusted_Score AS readmission_rate
    FROM {{ source('snowflake', 'NH_QUALITYMSR_CLAIMS') }}
    WHERE Measure_Description LIKE '%readmission%'
)
SELECT * FROM source