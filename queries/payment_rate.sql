SELECT
  p.payment_id,
  p.rental_id,
  r.rental_date,
  r.return_date,
  CASE
    WHEN r.return_date IS NULL THEN NULL
    ELSE (r.return_date::date > (r.rental_date::date + f.rental_duration))
  END AS is_overdue,
  CASE
    WHEN r.return_date IS NULL THEN NULL
    ELSE GREATEST(
           (r.return_date::date - (r.rental_date::date + f.rental_duration)),
           0
         )
  END AS days_overdue,               -- integer days
  f.film_id,
  f.title,
  f.rental_rate,
  p.amount AS paid_amount,
  (p.amount - f.rental_rate) AS delta
FROM payment p
JOIN rental   r ON r.rental_id = p.rental_id
JOIN inventory i ON i.inventory_id = r.inventory_id
JOIN film     f ON f.film_id = i.film_id
ORDER BY p.payment_id
LIMIT 50;
