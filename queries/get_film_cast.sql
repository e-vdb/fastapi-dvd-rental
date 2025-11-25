SELECT f.film_id, a.first_name, a.last_name
FROM film AS f
JOIN film_actor as fa
ON fa.film_id = f.film_id
JOIN actor as a
ON a.actor_id = fa.actor_id
WHERE f.film_id = 1;
