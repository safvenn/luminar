-- SUB-QUERIES---------------------------------------------------------

use practice1;
CREATE TABLE Employee(
    empid numeric(10),
    name varchar(20),
    salary numeric(10),
    department varchar(20)
);

CREATE TABLE Departments(
    deptid numeric(10),
    department varchar(20)
);

INSERT INTO Employee 
VALUES (100,"Jacob A",20000,"SALES"),(101,"James T",50000,"IT"),(102,"Riya S",30000,"IT");

INSERT INTO Departments 
VALUES (1,"IT"),(2,"ACCOUNTS"),(3,"SUPPORT");

select * from departments;
select * from Employee;


-- 1)

select * from employee where department=(select department from departments where deptid=1);

-- 2) salry less than avg 

select * from employee where salary<(select avg(salary) from employee);

-- 3) salry greater than avg 

select * from employee where salary>=(select avg(salary) from employee);

select * from customer5_windows;
-- 1)avg salry above salary f,l,age,pro,salry

select fname,lname,age,prof,salary from customer5_windows where salary > (select avg(salary) from customer5_windows);

-- 2)second highest salry f,l,age,pro,salary

select * from customer5_windows where (select max(salary) from customer5_windows)>salary order by salary desc limit 1;
