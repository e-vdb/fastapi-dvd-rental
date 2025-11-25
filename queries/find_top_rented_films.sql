SELECT COUNT(f.film_id), f.title, f.film_id
FROM rental as r
JOIN inventory as i
ON i.inventory_id = r.inventory_id JOIN film as f ON f.film_id=i.film_id
GROUP BY 2,3
ORDER BY 1 DESC
LIMIT 5;
