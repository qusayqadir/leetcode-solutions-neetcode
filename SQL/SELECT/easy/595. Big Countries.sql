-- Write your PostgreSQL query statement below
select w.name, w.population, w.area
from World as w 
WHERE w.area >= 3000000 or w.population >= 25000000; 