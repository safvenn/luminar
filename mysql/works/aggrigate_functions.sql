-- Agrigate Functions

use practice1;

-- 1.COUNT() -------------------------------------------------------------------------------------

-- to find total rows 

select count(*) as count from customer1;
select count(*) as count from  sample4;

-- to find count of coloumns

select prof,count(*) as count from customer1 group by prof order by count desc;

select loc,count(*) as count from customer1 group by loc order by count desc;

select prof,count(*) as count from customer1 where loc='india' group by prof order by count desc;

select age,count(*) as count from customer1 where loc='us' group by age order by count desc;

-- Having

select prof,count(*) as count from customer1 group by prof having count>10 order by count desc;

-- 2.MAX() ---------------------------------------------------------------------------------------------------------------

-- to find max value of a coloumn

select max(age) from customer1;
            
-- to find max from  a group

select prof,max(age) from customer1 group by prof;

-- by order

select prof,max(age)as max_age from customer1 group by prof order by max_age desc;

select loc,max(age) as max_age from customer1 where loc != '' group by loc order by max_age desc;

-- 3.MIN()  -----------------------------------------------------------------------------------------------------------------

select min(age) from customer1;

-- min age of each profession

select prof,min(age) from customer1 group by prof;

select prof,min(age)as min_age from customer1 group by prof order by min_age desc;

-- 4.SUM()  -----------------------------------------------------------------------------------------------------------------

select sum(age) from customer1;

select prof,sum(age) as Total from customer1 group by prof order by Total desc;

-- 5.AVG()  ----------------------------------------------------------------------------------------------------------------------

select avg(age) from customer1;

select prof,avg(age) as Avg from customer1 group by prof order by Avg desc;




