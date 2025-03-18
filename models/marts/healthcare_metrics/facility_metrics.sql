WITH bed_utilization AS (
    SELECT
        hospital_id,
        state,
        COALESCE(certified_beds, 1) AS certified_beds,  
        COALESCE(avg_residents_per_day, 0) AS avg_residents_per_day,  
        COALESCE(avg_residents_per_day, 0) / NULLIF(COALESCE(certified_beds, 1), 0) AS bed_utilization_rate
    FROM {{ ref('stg_provider_info') }}
)
SELECT * FROM bed_utilization
