-- ASSIGNMENT 2--------------------------------------------

use practice1;
select * from txn_windows;

-- 1. Find Row count

select count(*) from txn_windows;

-- 2. jan month oid,cusno,category,product,state

select oid,cuid,category,product,state,dat from txn_windows where  dat like '01%';

--  A. Row count

select count(*) from txn_windows where dat like '01%';

-- 3. July Month oid,cusno,category,product,state

select oid,cuid,category,product,state,dat from txn_windows where  dat like '07%';

--  B. Row count

select count(*) from txn_windows where dat like '07%';

-- 4. Each category [count desc sort]

select category,count(*) as count from txn_windows group by(category) order by count desc;

-- 5. Category full deatils

select * from txn_windows where category='Outdoor Recreation';

-- 6. Each paymethod count

select method,count(*) from txn_windows group by(method);

-- 7. jan-july month purchase count [include]

select count(*) from txn_windows where dat between '01-01-2011' and '07-31-2011';

-- 8. Each category total amount

select category , round(sum(pay_amount),2) as total from txn_windows group by(category) order by total desc;

-- 9. Each category maximum amount

select category , max(pay_amount) as max from txn_windows group by(category) order by max desc;

-- 10. Each category avg amount

select category , round(avg(pay_amount),2) as avg from txn_windows group by(category) order by avg desc;

-- 11.total amount by cash and credit card

select method , round(sum(pay_amount),2) as total from txn_windows group by(method) order by total desc;

-- 12. Indoor games ,total amount

select round(sum(pay_amount),2) as total from txn_windows where category='Indoor games';

-- 13. Each state count 

select state , count(*) as count from txn_windows group by(state) order by count desc;
