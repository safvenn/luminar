import pandas as pd 


df=pd.read_csv(r'C:\Desktop\luminar\Eda1\pandas1\files\customer1.csv')



data=df['fname'].str.startswith('A')

data1=df[data]['fname']

print(data1)