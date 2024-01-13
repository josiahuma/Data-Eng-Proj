-- payment method with the highest sales
SELECT payment_channel, MAX(total_price) highest FROM sales
GROUP BY payment_channel
ORDER BY 2 DESC;

-- price range analysis by brand
SELECT brand, price,
		CASE
		WHEN price BETWEEN 1000 AND 1500 THEN 'Low to Medium Price'
		WHEN price BETWEEN 1500 and 2000 THEN 'High Price'
		ELSE 'Very High Price'
		END AS price_range
FROM products
ORDER by price DESC;

-- retrieve product details and the corresponding staff information for each sale made
SELECT sa.sales_id, st.first_name ||' '||st.last_name full_name, 
pr.product_name, pr.brand, pr.model, sa.total_price 
FROM sales sa
JOIN staff st
ON st.staff_id = sa.staff_id
JOIN products pr
ON pr.product_id = sa.product_id;

-- retrieve amont each staff has sold
SELECT st.first_name ||' '||st.last_name full_name, SUM(sa.total_price) 
FROM sales sa
JOIN staff st
ON st.staff_id = sa.staff_id
GROUP BY full_name
ORDER BY 2 DESC;

-- best performing staff, staff with highest total sales
SELECT st.first_name ||' '||st.last_name full_name, SUM(sa.total_price)
FROM sales sa
JOIN staff st
ON st.staff_id = sa.staff_id
GROUP BY full_name
ORDER BY 2 DESC
LIMIT 1;

-- worst performing staff, staff with lowest total sales
SELECT st.first_name ||' '||st.last_name full_name, SUM(sa.total_price)
FROM sales sa
JOIN staff st
ON st.staff_id = sa.staff_id
GROUP BY full_name
ORDER BY 2
LIMIT 1;

-- best performing brand, brand with highest total sales
SELECT pr.brand, SUM(sa.total_price)
FROM sales sa
JOIN products pr
ON pr.product_id = sa.product_id
GROUP BY pr.brand
ORDER BY 2 DESC
LIMIT 1;

/* Get the product details and the names of the staff members
involved in each sale, including the transaction ID and payment
method.*/
SELECT st.first_name ||' '||st.last_name full_name, 
pr.product_name, pr.brand, pr.model, sa.sales_id, sa.payment_channel
FROM sales sa
JOIN staff st
ON st.staff_id = sa.staff_id
JOIN products pr
ON pr.product_id = sa.product_id;