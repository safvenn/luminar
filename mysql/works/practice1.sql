##SQL analissis using where condition--------------------------------------------------------------------------------------

use practice1;
show tables;
select * from sample4;
#age above 22--

select * from sample4 where age >22;

#age eauals to 21 ,fname,lname,age,phone-----

select fname,lname,age,phno from sample4 where age=21;

#loc==chennai-------

select fname,lname,age,phno from sample4 where loc='Chennai';

#more than 1 condition to check 

select * from sample4 where age>22 and loc='Chennai';

