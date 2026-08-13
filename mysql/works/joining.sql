-- JOINING -------------------------------------------------
use practice1;

-- 1)inner join
-- 2)left outer join
-- 3)right outer join
-- 4)full outer join

-- INNER JOINING-----------------------------------------------

select * from custom_windows c join order_windows o on(c.id=o.id);

select c.name,c.age,c.salary,o.dat,o.amount from custom_windows c join order_windows o on(c.id=o.id) where salary > 2000;

-- 1)age above 23 name,age,sala,loc,dat,amount

select c.name,c.age,c.salary,c.location,o.dat,o.amount from custom_windows c join order_windows o on(c.id=o.id) where c.age > 23;

-- 2)latest date 1 emp name ,age,salary,loc,dat,amnt

select c.name,c.age,c.salary,c.location,o.dat,o.amount from custom_windows c join order_windows o on(c.id=o.id) order by date(dat) desc limit 1;

-- 3)age minimum 1 emp name,age,salary,dat,amnt

select c.name,c.age,c.salary,o.dat,o.amount from custom_windows c join order_windows o on(c.id=o.id) order by age limit 1;

-- ---------------------------------------------------------------------------------------------------------------------------------------------------

-- 1)passed studnts name,roll,res

select s.name,s.roll,r.res from student s join result r on(s.roll=r.roll)where res ='pass';


-- LEFT OUTER JOINING---------------------------------------------------------------------------------------- 

select * from custom_windows c left join order_windows o on(c.id=o.id);

-- RIGHT OUTER JOINING----------------------------------------------------

select * from custom_windows c right join order_windows o on(c.id=o.id);

-- FULL OUTER JOINING-------------------------------------------------------------------

select * from custom_windows c right outer join order_windows o on(c.id=o.id) union select * from custom_windows c left outer join order_windows o on(c.id=o.id);


