#print 11 to 25

import pandas as pd

df=pd.read_csv(r'mysql\files\customer1.csv')


#print(df.iloc[11:26]) #print index 11 to 25


# df1=df.iloc[10:20,1:4]
# print(df1)


#x= last coloiumn expect
#y = last coloumn

x=df.iloc[:,0:5]
print(x)

y=df.iloc[:,-1]
print(y)