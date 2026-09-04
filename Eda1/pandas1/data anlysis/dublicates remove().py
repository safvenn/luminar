import pandas as pd 

df=pd.read_csv(r"C:\Desktop\luminar\Eda1\pandas1\files\customer1.csv")


#distinct == drop_dublicates()

df1=df.drop_duplicates()

print(sum(df.drop_duplicates()))




