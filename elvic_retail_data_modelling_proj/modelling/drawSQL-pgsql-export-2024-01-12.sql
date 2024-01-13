CREATE TABLE "products"(
    "product_id" VARCHAR(255) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "brand" VARCHAR(255) NOT NULL,
    "category" VARCHAR(255) NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "model" VARCHAR(255) NOT NULL,
    "price" DECIMAL(8, 2) NOT NULL
);
ALTER TABLE
    "products" ADD PRIMARY KEY("product_id");
CREATE TABLE "payment_method"(
    "payment_method_id" VARCHAR(255) NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "priority" INTEGER NOT NULL
);
ALTER TABLE
    "payment_method" ADD PRIMARY KEY("payment_method_id");
CREATE TABLE "customers"(
    "customer_id" VARCHAR(255) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "address" VARCHAR(255) NOT NULL,
    "phone_number" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "customers" ADD PRIMARY KEY("customer_id");
CREATE TABLE "orders"(
    "order_id" VARCHAR(255) NOT NULL,
    "order_date" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "delivery_address" VARCHAR(255) NOT NULL,
    "product_id" VARCHAR(255) NOT NULL,
    "customer_id" VARCHAR(255) NOT NULL,
    "quantity" INTEGER NOT NULL,
    "price" INTEGER NOT NULL,
    "location_id" VARCHAR(255) NOT NULL,
    "payment_id" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "orders" ADD PRIMARY KEY("order_id");
CREATE TABLE "location"(
    "location_id" VARCHAR(255) NOT NULL,
    "zip_code" VARCHAR(255) NOT NULL,
    "city" VARCHAR(255) NOT NULL,
    "state" VARCHAR(255) NOT NULL,
    "region" VARCHAR(255) NOT NULL,
    "country" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "location" ADD PRIMARY KEY("location_id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_customer_id_foreign" FOREIGN KEY("customer_id") REFERENCES "customers"("customer_id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_location_id_foreign" FOREIGN KEY("location_id") REFERENCES "location"("location_id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_product_id_foreign" FOREIGN KEY("product_id") REFERENCES "products"("product_id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_payment_id_foreign" FOREIGN KEY("payment_id") REFERENCES "payment_method"("payment_method_id");