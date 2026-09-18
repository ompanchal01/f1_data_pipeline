WITH sprint_qualy_source_data AS (
    SELECT 
        DISTINCT *
    FROM
        {{ source('raw_f1', 'sprint_qualy')}}
),

cleaned_sprint_qualy AS (
    SELECT 
	season,
	sprint_qualy_date,
	sprint_qualy_time,
	race_id,
	race_name,
	round,
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
	sprint_qualy_id,
	TO_CHAR(sq1, 'MI:SS:MS') AS s1,
	CASE WHEN sq2 IS NULL THEN 'NOT QUALIFIED' ELSE TO_CHAR(sq2, 'MI:SS:MS') END AS sq2,
	CASE WHEN sq3 IS NULL THEN 'NOT QUALIFIED' ELSE TO_CHAR(sq3, 'MI:SS:MS') END AS sq3,
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
	sprint_qualy_source_data
)

SELECT * FROM cleaned_sprint_qualy