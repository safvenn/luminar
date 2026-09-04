import numpy as np
import pandas as pd

#list to series

a=pd.Series([1,2,3,4,5,6,8,7],index=[1,0,7,6,5,4,3,2])  # chnage index only no chang ein element
print(a)

#tuple to series

a=pd.Series((1,2,3,4,5,6,8,7))
print(a)

a=pd.Series({'name':'safvan','age':21,"profession":"AI"},index=['age','profession','name'])  # index can chnage index order
print(a)


#prit dimention
print(a.ndim)


#print shape
print(a.shape)