# loc is used for filter  data


import pandas as pd

df=pd.read_csv(r'mysql\files\customer1.csv')

# df=df.loc[df['coloname']conditio]  --- syntax



# df1=df.loc[df['age']>22]

# df2=df[df['age']==21]

# print(df2)


#age equal to 21 fname , lanme,age


df1=df[df['age']==21][['fname','lname','age']]
print(df1)

#chennai work fname,lanme,age,phn

df2=df[df['loc']=='chennai'][['fname','lname','age']]
print(df2)

#age below 23 fname,lname,age

df3=df[df['age']<23][['fname','lname','age']]
print(df3)

#loc coloumns head/tail

df3=df[df['age']<23][['fname','lname','age']].head(10)
print(df3)
df3=df[df['age']<23][['fname','lname','age']].tail(5)
print(df3)


#chennai work and age age above 23

df1=df.loc[(df['loc']=='chennai')&(df['age']>23)]
print(df1)