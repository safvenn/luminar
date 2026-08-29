import pandas as pd 

import numpy as np  



a=pd.Series([10,20,30,40,50,60,70])
b=pd.Series([5,10,15,20,25,30])


#addititon




c=a.add(b)
print(c)

# 0    15.0
# 1    30.0
# 2    45.0
# 3    60.0
# 4    75.0
# 5    90.0
# 6     NaN    -----> if missing values 
# dtype: float64

print('* - arithmetic operations.py:28'*100)

#substraction

s=a.sub(b)
print(s)

print('* - arithmetic operations.py:35'*100)

#multiplication

mul=a.multiply(b)
print(mul)



print('* - arithmetic operations.py:44'*100)

#division

div=a.divide(b)
print(div)

print('* - arithmetic operations.py:51'*100)

