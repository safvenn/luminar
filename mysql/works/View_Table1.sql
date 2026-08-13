#VIEW TABLE 
# agge less than 24

# create view table

create view age_data as select * from sample4 where age >22;  

# Show results

select * from age_data;

show tables;

#store chennai work data age above 22 fname,lname,age,phon 

create view chennai_22 as select fname,lname,age,phno from sample4 where loc='Chennai' and age>22;

select * from chennai_22;

#Drop a view table----------------------------------

drop view age_data; 