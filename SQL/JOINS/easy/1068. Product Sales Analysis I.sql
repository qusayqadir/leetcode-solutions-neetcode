-- Write your PostgreSQL query statement below
select p.product_name, s.year, s.price
FROM sales as s
JOIN product as p 
    on p.product_id = s.product_id 

where sale_id is not null 

