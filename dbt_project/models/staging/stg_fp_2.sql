WITH free_practice_2_source_data AS (
    SELECT 
        DISTINCT *
    FROM
        {{ source('raw_f1', 'free_practice_2')}}
),

cleaned_fp_2 AS (
    SELECT 
        season,
        round,
        fp_date,
        fp_time,
        race_id,
        race_name,
        circuit_id,
        circuit_name,
        country,
        city,
        REPLACE(circuit_length, 'km', 'm') AS circuit_length,
        lap_record::TIME AS lap_record,
        first_participation_year,
        corners,
        fastest_lap_driver_id,
        fastest_lap_team_id,
        fastest_lap_year,
        fp_id,
        time::TIME AS lap_time,
        driver_id,
        driver_name, 
        driver_surname,
        driver_nationality,
        CASE WHEN driver_number IS NULL THEN 0 ELSE driver_number END AS driver_number,
        driver_short_name,
        driver_birthday,
        team_id,
        team_name, 
        team_nationality,
        first_appearance,
        CASE WHEN constructors_championships IS NULL THEN 0 ELSE constructors_championships END AS constructors_championships,
        CASE WHEN drivers_championships IS NULL THEN 0 ELSE drivers_championships END AS drivers_championships
    FROM 	
        free_practice_2_source_data
)

SELECT * FROM cleaned_fp_2