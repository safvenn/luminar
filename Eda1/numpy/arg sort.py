import numpy as np


#arg generates index


# a=np.array([6,5,6,8,6,4,3])
#
# b=np.argsort(a)
# print(b)

# [6 5 1 0 4 2 3]


#arg sort on 2 dimnetion

a=np.array([[4,5,6,1],[1,2,3,4],[6,7,8,3],[7,6,5,4],[1,3,5,7]])

b=np.argsort(a)
print(b)
print('*'*100)
#coloumn wise arg sort

a=np.array([[4,5,6,1],[1,2,3,4],[6,7,8,3],[7,6,5,4],[1,3,5,7]])

b=np.argsort(a,axis=0)
print(b)

