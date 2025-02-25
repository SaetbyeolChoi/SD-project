WITH state_avg AS (
    SELECT 
        State, 
        AVG(Adjusted_Score) AS avg_readmission_rate
    FROM {{ source('snowflake', 'NH_QUALITYMSR_CLAIMS') }}
    WHERE Adjusted_Score IS NOT NULL
    GROUP BY State
),

source AS (
    SELECT
        q.CCN AS hospital_id,
        q.State AS state,
        q.Measure_Description AS diagnosis_category,
        COALESCE(q.Adjusted_Score, sa.avg_readmission_rate) AS readmission_rate
    FROM {{ source('snowflake', 'NH_QUALITYMSR_CLAIMS') }} q
    LEFT JOIN state_avg sa ON q.State = sa.State
)
SELECT * FROM source