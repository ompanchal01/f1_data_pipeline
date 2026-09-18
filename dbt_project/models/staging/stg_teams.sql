WITH teams_source_data AS (
    SELECT 
        DISTINCT *
    FROM 
        {{ source('raw_f1', 'teams') }}
),

cleaned_teams AS (
    SELECT 
	teams_id,
    team_name,
    team_nationality,
    first_appeareance,
    CASE WHEN constructors_championships IS NULL THEN 0 ELSE constructors_championships END AS constructors_championships,
	CASE WHEN drivers_championships IS NULL THEN 0 ELSE drivers_championships END AS drivers_championships
FROM 	
	teams_source_data
)

SELECT * FROM cleaned_teams