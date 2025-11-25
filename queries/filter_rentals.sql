SELECT rental_id, customer_id, inventory_id
FROM rental
WHERE customer_id = 6
ORDER BY rental_id
OFFSET 0
LIMIT 5;
