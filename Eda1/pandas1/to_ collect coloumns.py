import pandas as pd

df=pd.read_csv(r'mysql\files\customer1.csv')



df1=df[['fname','lname','age','prof']]  #returns specific colounms
print(df1)


#print last 25 fname,lanme,age,prof


df2=df[['fname','lname','age','prof']].head(25)
print(df2)

print("_____________________________________________________________________________________________________________ - to_ collect coloumns.py:17")

#last 10 fname,lanme,age


df3=df[['fname','lname','age','prof']].tail(10)
print(df3)
