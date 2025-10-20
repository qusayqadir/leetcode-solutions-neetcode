-- Write your PostgreSQL query statement below
select eu.unique_id, e.name
from Employees as e 
    LEFT JOIN EmployeeUNI eu 
    ON eu.id = e.id
order by unique_id

