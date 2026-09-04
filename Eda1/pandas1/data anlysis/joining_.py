import os

os.system("cls")


import pandas as pd 

x='*'*100

df=pd.read_csv(r"C:\Desktop\luminar\Eda1\pandas1\files\student.csv")
df1=pd.read_csv(r"C:\Desktop\luminar\Eda1\pandas1\files\result.csv")





ress=pd.merge(df,df1,on='roll',how='inner').loc[df1['res']=='pass']
print(ress)