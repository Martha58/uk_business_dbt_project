WITH unique_cities AS (
    SELECT DISTINCT city 
    FROM main.local_business
)

SELECT * FROM unique_cities
