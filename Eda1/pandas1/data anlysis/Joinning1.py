import os

os.system("cls")
x='*'*100
import pandas as pd 


lst=[[101,'vijay','k',21],
     [102,'akil','m',23],
     [103,'ammu','ks',21],
     [105,'safvan','k',21],
     [104,'shiyas','m',23],
     [106,'rishana','vt',24]
     ]


df=pd.DataFrame(lst)
df.columns=['id','fname','lname','age']

#print(df)

lst1=[
    ['python',101,'mannarkkad',10000],
    ['django',102,'Kozhikode',15000],
    ['ds',103,'ernamkulam',50000],
    ['AI',104,'palakkad',32000],
    ['ML',105,'cherpulasheri',110000]
]


df1=pd.DataFrame(lst1)

df1.columns=['profession','id','location','salary']

#print(df1)


#inner joining -- joins by matching coloumns value  -----------------------------------------------------------------------------

df2=pd.merge(df,df1,on='id',how='inner')

df3=df.merge(df1,on='id',how='inner').loc[df['age']>20]

# print(df3)


#age max 1 emp  fname, lname, age, prof,location


max_age=pd.merge(df,df1,on='id',how='inner').sort_values(by='age',ascending=False).head(1)[['fname','lname','age','profession','location']]
#print(max_age)




#Each prof count

prof_count=pd.merge(df,df1,on='id',how='inner').groupby('profession')['profession'].count()

print(prof_count)

x='*'*100
print(x)

#left outeer join-----------------------------------------------------------------------------------------------------------

#return all ddata fro left and matching data from right others return null.

left=pd.merge(df,df1,on='id',how='left')
print(left)

print(x)
#rigt outer join-----------------------------------------------------------------------------------------------


right=pd.merge(df,df1,on='id',how='right')
print(right)
print(x)



#full pouter joining------------------------------------------------------------------------------------------------

full=pd.merge(df,df1,on='id',how='outer')
print(full)