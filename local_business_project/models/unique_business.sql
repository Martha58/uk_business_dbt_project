WITH unique_business AS (
    SELECT DISTINCT business
    FROM main.local_business
)

SELECT * FROM unique_business