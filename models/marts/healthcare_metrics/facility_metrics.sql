WITH bed_utilization AS (
    SELECT
        hospital_id,
        state,
        certified_beds,  
        avg_residents_per_day,  
        avg_residents_per_day / NULLIF(certified_beds, 0) AS bed_utilization_rate
    FROM {{ ref('stg_provider_info') }}
)
SELECT * FROM bed_utilization