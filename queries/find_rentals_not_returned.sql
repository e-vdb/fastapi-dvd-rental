SELECT r.rental_id, r.rental_date, r.inventory_id, i.film_id, f.rental_rate, f.rental_duration
FROM rental AS r
JOIN inventory AS i
ON i.inventory_id = r.inventory_id
JOIN film AS f
ON i.film_id = f.film_id
WHERE return_date IS NULL;
