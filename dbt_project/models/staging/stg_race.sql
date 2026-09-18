WITH race_source_data AS (
    SELECT 
        DISTINCT *
    FROM
        {{ source('raw_f1', 'race')}}
),

cleaned_race AS (
    SELECT 
	season,
	round,
	race_date,
	race_time,
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
	CASE WHEN position IS NULL OR position = '-' THEN 'DNF' ELSE position END AS position,
	points,
	grid,
	CASE WHEN fast_lap IS NULL THEN 'NO LAP SET' ELSE TO_CHAR(fast_lap, 'MI:SS:MS') END AS fast_lap,	
	CASE WHEN retired IS NULL THEN 'ACTIVE' ELSE retired END AS retired,
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
	race_source_data
)

SELECT * FROM cleaned_race