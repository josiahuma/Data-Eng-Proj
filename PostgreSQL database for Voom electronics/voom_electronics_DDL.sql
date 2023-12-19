CREATE TABLE sale(
    sales_id INT NOT NULL PRIMARY KEY,
    product_id INT,
    customer_id INT,
    staff_id INT,
    quantity INT,
    selling_price DECIMAL(10,2),
    discount DECIMAL(10,2),
    total_price DECIMAL(10,2),
    payment_method VARCHAR(50),
    sale_date DATE
);

CREATE TABLE staff(
    staff_id INT NOT NULL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    position VARCHAR(50),
    contact_number VARCHAR(20),
    staff_email VARCHAR(100)
);

CREATE TABLE customer(
    customer_id INT NOT NULL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    address VARCHAR(255),
    phone_number VARCHAR(20)
);

CREATE TABLE product(
    product_id INT NOT NULL PRIMARY KEY,
    product_name VARCHAR(50),
    brand VARCHAR(50),
    model VARCHAR(50),
    type VARCHAR(50),
    size INT,
    price DECIMAL(10,2),
    description TEXT,
    warranty_period VARCHAR(255)
);