#head to print first elements

import pandas as pd

a=pd.Series([10,20,30,40,50,60])


print(a.head())  #default =5

print(a.head(1))



# tail()

# print last  elemnts

print(a.tail(3))