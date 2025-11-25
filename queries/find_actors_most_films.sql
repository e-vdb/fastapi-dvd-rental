SELECT COUNT(f.film_id), a.first_name, a.last_name, a.actor_id
FROM film_actor as f
JOIN actor as a
ON f.actor_id = a.actor_id
GROUP BY 2,3,4
ORDER BY 1 DESC
LIMIT 10;
