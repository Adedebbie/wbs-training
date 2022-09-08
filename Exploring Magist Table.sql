-- 1) how many orders are there in the data set?
SELECT count(*)
FROM orders;
-- ans; 99,441

-- 2) ARE ORDERS ACTUALLY DELIVERED?
SELECT DISTINCT count(order_status), order_status
FROM orders
group by order_status;
-- delivered : 96,478
-- unavailable: 609
-- shipped: 1107
-- cancelled: 625
-- invoiced: 314
-- processing: 301
-- approved: 2
-- created: 5

-- 3) Is Magist having user growth?
SELECT MONTH(order_purchase_timestamp) AS 'MONTH', YEAR(order_purchase_timestamp) AS 'YEAR', COUNT(customer_id)
FROM orders
GROUP BY MONTH(order_purchase_timestamp), YEAR(order_purchase_timestamp)
ORDER BY YEAR, MONTH;

-- 4) How many products are there on the products table?
-- count number of duplicates
SELECT product_id, COUNT(product_id)
FROM products
GROUP BY product_id
HAVING COUNT(product_id) > 1;

-- count number of prducts are in products table
SELECT 
    COUNT(DISTINCT product_id) AS products_count
FROM
    products;

-- 5) Which are the categories with the most products? 
SELECT count(product_id),product_category_name
FROM products p
GROUP BY p.product_category_name;
-- ans : cama_mesa_banho 3029
-- OR 
SELECT 
    product_category_name, 
    COUNT(DISTINCT product_id) AS n_products
FROM
    products
GROUP BY product_category_name
ORDER BY COUNT(product_id) DESC;


-- 6) How many of those products were present in actual transactions? 
SELECT count(DISTINCT oi.product_id)
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id;
-- ans : 32951
SELECT 
	count(DISTINCT product_id) AS n_products
FROM
	order_items;
-- 7) What’s the price for the most expensive and cheapest products?
SELECT MAX(price) AS 'Most expensive', MIN(price) AS 'cheapest'
FROM order_items;
-- ANS: 6735, 0.85 respectively

-- 8) What are the highest and lowest payment values? 
SELECT MAX(payment_value) AS 'Max amount paid',MIN(payment_value) AS 'Min amount paid'
FROM order_payments
-- Ans: 13664.1



