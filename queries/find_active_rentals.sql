SELECT
  r.rental_id,
  r.customer_id,
  r.rental_date,
  i.film_id,
  i.inventory_id,
  f.rental_duration,
  (r.rental_date::date + f.rental_duration) AS due_date,
  (current_date > (r.rental_date::date + f.rental_duration)) AS is_overdue,
  GREATEST(
    (current_date - (r.rental_date::date + f.rental_duration)),
    0
  ) AS days_overdue
FROM rental AS r
JOIN inventory AS i ON i.inventory_id = r.inventory_id
JOIN film      AS f ON f.film_id      = i.film_id
WHERE r.return_date IS NULL
ORDER BY r.rental_id DESC;
