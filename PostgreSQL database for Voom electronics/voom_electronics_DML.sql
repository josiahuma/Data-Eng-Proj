-- insert into sales table
INSERT INTO sales(sales_id, product_id, customer_id, staff_id, quantity, selling_price, discount, total_price, payment_method, sale_date) VALUES
(10923, 201, 42, 502, 2, 4500, 0, 3000, 'paypal', '7/7/2022'),
(10924, 201, 42, 502, 2, 4500, 0, 3000, 'paypal', '7/7/2022');

-- alter customers table and add location
ALTER TABLE customers
ADD location VARCHAR(100);

-- update location in customers table to FCT
UPDATE customers
SET location = 'FCT';

-- rename column payment method to payment channel
ALTER TABLE sales RENAME COLUMN payment_method TO payment_channel;

-- adding forign keys to table sales
ALTER TABLE sales
ADD FOREIGN KEY (product_id) REFERENCES products(product_id);

ALTER TABLE sales
ADD FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

ALTER TABLE sales
ADD FOREIGN KEY (staff_id) REFERENCES staff(staff_id);

