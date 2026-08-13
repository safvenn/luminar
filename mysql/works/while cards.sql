-- WHILE CARDS---------------------------------------------------------------------------------------------------------

-- BETWEEN---------------------------------

use practice1;

select * from customer1 where age between 30 and 40;

-- NOT BETWEEN---------------------------------

select * from customer1 where age not between 30 and 40;

-- LIKE--------------------------------------------

-- fname end from e
select * from customer1 where fname like '%e';
-- fname start from a
select * from customer1 where fname like 'a%';
-- second char is a ( '_' used for char space)
select * from customer1 where fname like '_a%';
-- contains
select * from customer1 where fname like '%e%';