WITH staffing_ratio AS (
    SELECT
        hospital_id,
        state,
        month,
        SUM(rn_hours_emp) + SUM(lpn_hours_emp) + SUM(cna_hours_emp) AS total_permanent_hours,
        SUM(rn_hours_contract) + SUM(lpn_hours_contract) + SUM(cna_hours_contract) AS total_contract_hours,
        CASE 
            WHEN COALESCE(SUM(rn_hours_contract) + SUM(lpn_hours_contract) + SUM(cna_hours_contract), 0) = 0 
            THEN NULL  
            ELSE (SUM(rn_hours_emp) + SUM(lpn_hours_emp) + SUM(cna_hours_emp)) / 
                 (SUM(rn_hours_contract) + SUM(lpn_hours_contract) + SUM(cna_hours_contract))
        END AS permanent_to_contract_ratio
    FROM MYDB_H.MY_SCHEMA_H_staging.stg_pbj_nurse_staffing
    GROUP BY hospital_id, state, month
)
SELECT * FROM staffing_ratio