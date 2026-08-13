#Questions -practice


#1. age mini 2 emp f,lage,phno

select fname,lname,phno from sample4 order by age  limit 2;

#2.age mxm 1 emp fname, lname,age phno

select fname,lname,age,phno from sample4 order by age desc limit 1;

#3.chennai work,age mxm 1 emp f,l,age,phno

select fname,lname,age,phno from sample4 where loc='Chennai' order by age desc limit 1;

#4.age mxm 2 emp f,l,age==>result store

create view topage_2_emp as select fname,lname,age from sample4 order by age desc limit 2;

#show

select * from topage_2_emp;