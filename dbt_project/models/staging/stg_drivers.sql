WITH drivers_source_data AS (
    SELECT 
        DISTINCT *
    FROM 
        {{ source('raw_f1', 'drivers') }}
),

cleaned_drivers AS (
    SELECT 
        driver_id,
        CONCAT (driver_name,' ',driver_surname) AS driver_fullname,
        driver_nationality,
        driver_birthdate,
        driver_number,
        driver_short_name,
        team_id
    FROM 
        drivers_source_data
)

SELECT * FROM cleaned_drivers