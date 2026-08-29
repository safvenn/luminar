import pandas as pd


df=pd.read_csv(r'C:\Desktop\luminar\Eda1\pandas1\files\sample4.txt',sep=',',header=None)
df.columns=['id','fname','lname','age','phno','location']
print(df)