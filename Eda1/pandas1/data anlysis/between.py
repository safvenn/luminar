import pandas as pd 


df=pd.read_csv(r'C:\Desktop\luminar\Eda1\pandas1\files\customer1.csv')

df1=df['age'].between(25,40,inclusive=True)

print(df1)





#Between must both right and left table data type is numeric