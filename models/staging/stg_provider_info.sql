WITH source AS (
    SELECT
        CCN AS hospital_id,
        Provider_Name AS hospital_name,
        State AS state,
        Number_of_Certified_Beds AS certified_beds,
        COALESCE(Average_Number_of_Residents_per_Day, 0) AS avg_residents_per_day 
    FROM {{ source('snowflake', 'NH_PROVIDERINFO') }}
)
SELECT * FROM source
