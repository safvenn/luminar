#ORDER BY ----------------------------------------------

select * from sample4 order by age;


#for decsending -----------------------------

select * from sample4 order by age desc;


#also works with stings A-Z  ---------------------------------------


select * from sample4 order by fname;


#HEIRACHY
# [SELCT > WHERE > ORDER BY > LIMIT]


#LOC == CHENNAI ORDER BY AGE

select * from sample4 where loc='Chennai' order by age desc;