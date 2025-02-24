WITH source AS (
    SELECT 
        PROVNUM AS hospital_id,
        PROVNAME AS hospital_name,
        STATE AS state,
        DATE_TRUNC('MONTH', WorkDate) AS month,
        Hrs_RN AS rn_hours,
        Hrs_LPN AS lpn_hours,
        Hrs_CNA AS cna_hours,
        Hrs_RN_emp AS rn_hours_emp,
        Hrs_RN_ctr AS rn_hours_contract
    FROM {{ source('snowflake', 'PBJ_DAILY_NURSE_STAFFING') }}
)
SELECT * FROM source
