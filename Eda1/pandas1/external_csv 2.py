import pandas as pd

df=pd.read_csv(r'mysql\files\customer1.csv')

print(df)

print(df.head(10))

print("* - external_csv 2.py:9"*100)

print(df.tail(10))


