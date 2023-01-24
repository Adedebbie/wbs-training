USE sales_db;
-- Let’s consider store 20. What was the total (rounded) profit of this store? 
SELECT ROUND(SUM(weekly_sales), 2)
from sales_exercise
WHERE store = 20;
-- ans '301397792.46'

-- What was the total profit for department 51 (store 20)?
SELECT ROUND(SUM(weekly_sales), 2)
from sales_exercise
WHERE dept = 51 AND store = 20;
-- AANS:'161.18'

-- In which week did store 20 achieve a profit record (for the whole store)? How much profit did they make?
SELECT  ROUND(SUM(weekly_sales),2),  Date
from sales_exercise
WHERE store  = 20 
group by date 
ORDER BY SUM(weekly_sales) desc;

-- Which was the worst week for store 20 (for the whole store)? How much was the profit?
SELECT  ROUND(SUM(weekly_sales),1), Date
from sales_exercise
WHERE store  = 20 
GROUP BY date
ORDER BY SUM(weekly_sales) ASC;

-- What is the (rounded) average of the weekly sales for store 20 (the whole store)?
SELECT ROUND(AVG(week_sales),1) AS  avg_sales -- ,  Date
FROM (
SELECT store, date, SUM(weekly_sales) as week_sales
FROM sales_exercise `sales data-set`
WHERE store  = 20
GROUP BY store,date) a;
-- ans: '2107676.9'


-- alternative

SELECT round(SUM(weekly_sales)/count(distinct(date)))
from sales_exercise
where store = 20;
-- ans '2107677'


-- ORDER BY weekly_sales asc

-- What are the 3 stores that have the best historical average of weekly sales?
SELECT  AVG(weekly_sales),store
FROM sales_exercise
GROUP BY store 
ORDER BY AVG(weekly_sales) DESC
LIMIT 3;
-- ans: 20,4,14

-- Which departments from store 20 were the best and the worst in terms of overall sales?
SELECT dept, ROUND(SUM(weekly_sales)) AS overall_sales
FROM sales_exercise
WHERE store = 20
GROUP BY dept
ORDER BY overall_sales DESC
LIMIT 1 ;
-- ans;92
-- worst 
SELECT dept, SUM(weekly_sales) AS overall_sales
FROM sales_exercise
WHERE store = 20
GROUP BY dept
ORDER BY overall_sales ASC
LIMIT 1 ;
-- ANS 47

-- How much profit does the average department make in store 20?
SELECT SUM(weekly_sales)/ count(distinct dept)
FROM sales_exercise
where store = 20;
-- '3864074.262307689'
/*
Consider store 20. 
Calculate the difference between the total profit of each department and the total profit of the average department. 
This will be the departments’ “performance metric”. Which department is the worst performer and what’s its performance?
*/
-- total profit for each department 
SELECT  dept ,store, (sum(weekly_sales)-
(SELECT SUM(weekly_sales)/count(distinct dept) 
FROM sales_exercise where store = 20)) as performance
FROM sales_exercise 
WHERE store = 20
group by dept, store
order by performance asc
LIMIT 1;
-- ANS:'47', '20', '-3864452.842307689'

/*
Which department-store combination is the overall best performer (and what’s its performance?)? 
Consider the performance metric from the previous question, that is, 
the difference between a department’s sales and the sales of the average department of the corresponding store.
*/

SELECT  dept , store, (sum(weekly_sales)-
(SELECT SUM(weekly_sales)/count(distinct dept)
FROM sales_exercise WHERE store = 20)) as performance
FROM sales_exercise 
group by dept, store
order by performance desc
LIMIT 1;

-- Alternative
SELECT Dept, Store, SUM(Weekly_Sales) - AVG(SUM(Weekly_Sales)) OVER (PARTITION BY Store) AS sales_difference
FROM sales_exercise
GROUP BY Dept, Store
ORDER BY sales_difference DESC
LIMIT 1;


