WITH staffing_ratio AS (
    SELECT
        hospital_id,
        state,
        month,
        SUM(rn_hours_emp) AS total_rn_hours_emp,
        SUM(lpn_hours) AS total_lpn_hours,
        SUM(cna_hours) AS total_cna_hours,
        SUM(rn_hours_contract) AS total_rn_hours_contract,
        CASE 
            WHEN COALESCE(SUM(rn_hours_contract), 0) = 0 
            THEN 0  -- If no contract nurses, set ratio to 0
            ELSE COALESCE(SUM(rn_hours_emp + lpn_hours + cna_hours), 0) / SUM(rn_hours_contract)
        END AS permanent_to_contract_ratio

    FROM {{ ref('stg_pbj_nurse_staffing') }}
    GROUP BY hospital_id, state, month
)
SELECT * FROM staffing_ratio