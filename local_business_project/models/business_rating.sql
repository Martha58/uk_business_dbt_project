WITH bad_rating AS (
    SELECT 
    name, 
    city,
    rating, 
    types
    FROM main.local_business
    WHERE rating <= 3
    ORDER BY rating DESC
),

good_rating AS (
    SELECT 
    name, 
    city,
    rating, 
    types
    FROM main.local_business
    WHERE rating >= 3.1
    ORDER BY rating DESC
)

SELECT * FROM good_rating
UNION ALL
SELECT * FROM bad_rating