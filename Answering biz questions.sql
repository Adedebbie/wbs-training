/* IN RELATION TO THE PRODUCTS*/

-- What categories of tech products does Magist have
SELECT product_category_name_english 
FROM product_category_name_translation
WHERE product_category_name_english IN ('console_games', 'electronics', 'computers_accessories', 'pc_gamer', 'computers', 'tablets_printing_image', 'telephony', 'fixed_telephony');

SELECT DISTINCT COUNT(p.product_category_name) AS 'no of products', p.product_category_name, product_category_name_english
FROM  products p
JOIN product_category_name_translation pcnt
ON p.product_category_name = pcnt.product_category_name
WHERE product_category_name_english IN ('console_games', 'electronics', 'computers_accessories', 'pc_gamer', 'computers', 'tablets_printing_image', 'telephony', 'fixed_telephony')
GROUP BY p.product_category_name
ORDER BY COUNT(p.product_category_name) DESC;
-- ANS: 
-- Computer accessories ; 1639
-- telephony: 1134
-- electronics: 517
-- fixed_telephony: 116
-- computers: 30
-- tablet printing image: 9
-- pc gamer: 3


-- How many products of these tech categories have been sold (within the time window of the database snapshot)? 
-- What percentage does that represent from the overall number of products sold?
-- What’s the average price of the products being sold?
-- Are expensive tech products popular? 
/* TIP: Look at the function CASE WHEN to accomplish this task.t have?*/

 