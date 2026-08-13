-- Questions 3

use practice1;

-- 1. Each row count

select count(distinct id) from customer5_windows;

-- 2. each profession count [count desc order]

select prof,count(prof ) as count from customer5_windows group by prof order by count desc;

-- 3. each prof max salary [desc]

select prof,max(salary) as max_salry from customer5_windows group by prof order by max_salry desc;

-- 4. each loc min salary [acc]

select loc,min(salary) as min_salry from customer5_windows group by loc order by min_salry;

-- 5. each prof total salry [desc]

select prof,max(salary) as total_salry from customer5_windows group by prof order by total_salry desc;

-- 6. india work,each prof max salry [desc]

select prof,max(salary) as max_salry from customer5_windows where loc='india' group by prof order by max_salry desc;

-- 7. each profession avg salry 

select prof,round(avg(salary),2) as avg_salry from customer5_windows group by prof order by avg_salry desc;