

import pandas as pd

df=pd.read_csv(r'mysql\files\customer1.csv')

#Total missing values

print(df.isna().sum())

#fillna()

df1=df.fillna('india')
print(df1.isna().sum())