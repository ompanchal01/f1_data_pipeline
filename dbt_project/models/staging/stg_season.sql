WITH season_source_data AS (
    SELECT 
        DISTINCT *
    FROM 
        {{ source('raw_f1', 'season') }}
),

cleaned_season AS (
    SELECT 
	championship_id,
    championship_name,
    year
FROM 	
	season_source_data
)

SELECT * FROM cleaned_season