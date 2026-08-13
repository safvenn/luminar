-- QUESTIONS 2 --

use practice1;
-- 1.Age below 50 fname,lanme,age,prof ==store

create view age_50 as select fname,lname,age,prof from customer1 where age<50;
select * from age_50;

-- 2.Age above 69 fname,lname,age,prof

select fname,lname,age,prof from customer1 where age>69;

-- 3.india work fname,lname,age,prof

select fname,lname,age,prof from customer1 where loc='india';

-- 4.india work and age above 50 fname,lname,age,prof

select fname,lname,age,prof from customer1 where loc='india' and age>50;

-- 5.age maximum 5 emp fname,lname,age,prof

select fname,lname,age,prof from customer1 order by age desc limit 5;

-- 6.age minimum 3 emp f,l,a,p == store
 
create view mini_age as select fname,lname,age,prof from customer1 order by age limit 3;
select * from mini_age;

-- 7.inida work and prof doc  f,l,a,p

select fname,lname,age,prof from customer1 where loc='india' and prof ='Doctor';

-- 8.india work and prof doc,age mxm 1 emp f,l,a,p

select fname,lname,age,prof from customer1 where loc='india' and prof ='Doctor' order by age desc limit 1;

-- 9.pilot prof ,age minimum 1 emp fname,lname,age

select fname,lname,age,prof from customer1 where prof ='Doctor' order by age limit 1;

-- 10.uk work ,age minimum 10 emp fname,lnmae,age,prof

select fname,lname,age,prof from customer1 where loc='uk' order by age limit 10;