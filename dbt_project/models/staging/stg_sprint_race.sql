WITH sprint_race_source_data AS (
    SELECT 
        DISTINCT *
    FROM
        {{ source('raw_f1', 'sprint_race')}}
),

cleaning AS (
    SELECT 
		season,
		sprint_race_date,
		sprint_race_start_time,
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
		sprint_race_id,
		position,
		points,
		grid,
		laps,
		time AS raw_time,  -- Kept so "+1 lap" or "DNF" can be returned as text
        CASE 
            WHEN time ~ '^\+[0-9]+:[0-9]+(\.[0-9]+)?$' THEN ('00:' || ltrim(time, '+'))::interval
            WHEN time ~ '^\+[0-9]+(\.[0-9]+)?$' THEN ('00:00:' || ltrim(time, '+'))::interval
            WHEN time ~ '^[0-9]+:[0-9]+(\.[0-9]+)?$' THEN ('00:' || time)::interval
            ELSE NULL
        END AS step_interval_time,
		CASE WHEN retired IS NULL THEN 'ACTIVE' ELSE retired END AS retired,
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
		sprint_race_source_data
),

cleaned_sprint_race AS (
	SELECT 
    season,
    sprint_race_date,
    sprint_race_start_time,
    race_id,
    race_name,
    round,
    circuit_id,
    circuit_name,
    country,
    city,
    circuit_length,
    lap_record,
    first_participation_year,
    corners,
    fastest_lap_driver_id,
    fastest_lap_team_id,
    fastest_lap_year,
    sprint_race_id,
    position,
    points,
    grid,
    laps,
    CASE 
        WHEN step_interval_time IS NOT NULL THEN 
            TO_CHAR(
                SUM(step_interval_time) OVER (
                    PARTITION BY race_id
                    ORDER BY position 
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ), 
                'MI:SS.MS'
            )
        ELSE raw_time  
    END AS time,
    retired,
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
    constructors_championships,
    drivers_championships
FROM 
    cleaning
)

SELECT * FROM cleaned_sprint_race