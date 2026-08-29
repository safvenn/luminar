#where

import numpy as np

# a = np.array([1, 2, 3, 4, 5, 6, 7, 8])
#
# b=np.where(a>3)
# c=np.where(a==4)
# print(c)
# print(b)

# output
# (array([3]),)
# (array([3, 4, 5, 6, 7]),)
#
# it return the index of the array


# 2 diamentional arrayy


# a= np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
# b=np.where(a>10)
#
# print(b)

#output
   #coloumn index   #row index
# (array([2, 2]),   array([2, 3]))




#COLLECT ELEMENTS LIKE FILTER

a = np.array([1, 2, 3, 4, 5, 6, 7, 8])
b=a>5
c=a[b]
print(c)

