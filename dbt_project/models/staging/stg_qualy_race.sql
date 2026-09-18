WITH qualy_race_source_data AS (
    SELECT 
        DISTINCT *
    FROM
        {{ source('raw_f1', 'qualy_race')}}
),

cleaned_qualy_race AS (
    SELECT 
        season,
        round,
        qualy_time,
        qualy_date,
        race_id,
        race_name,
        circuit_id,
        circuit_name,
        country,
        city,
        REPLACE(circuit_length, 'km', 'm') AS circuit_length,
        lap_record,
        first_participation_year,
        corners,
        fastest_lap_driver_id,
        fastest_lap_team_id,
        fastest_lap_year,
        classification_id,
        q1,
        CASE WHEN q2 IS NULL THEN 'ELIMINATED' ELSE q2 END AS q2,
        CASE WHEN q3 IS NULL THEN 'ELIMINATED' ELSE q3 END AS q3,
        grid_position,
        driver_id,
        driver_name, 
        driver_surname,
        driver_nationality,
        driver_number,
        driver_short_name,
        driver_birthday,
        team_id,
        team_name, 
        team_nationality,
        first_appearance,
        CASE WHEN constructors_championships IS NULL THEN 0 ELSE constructors_championships END AS constructors_championships,
        CASE WHEN drivers_championships IS NULL THEN 0 ELSE drivers_championships END AS drivers_championships
    FROM 	
        qualy_race_source_data
)

SELECT * FROM cleaned_qualy_race