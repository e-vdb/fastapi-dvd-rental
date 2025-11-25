SELECT f.film_id, f.title, c.name AS category
FROM film AS f
JOIN film_category AS fc
ON fc.film_id = f.film_id
JOIN category AS c
ON c.category_id = fc.category_id
ORDER BY 2;
