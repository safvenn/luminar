#sort
import numpy as np

#sort one dimention ------------------------

#Assending

# a=np.array([6,5,6,8,6,4,3])
#
# s=np.sort(a)
# print(s)
#
# # desending
#
# d=np.sort(a)[::-1]
#
# print(d)

#sort in two dimention--------------------------------------------

#Deafault sort order on row on asscending order

#order by row wise

a=np.array([[4,5,6,1],[1,2,3,4],[6,7,8,3],[7,6,5,4],[1,3,5,7]])
b=np.sort(a)
print(b)

print('*'*100)


#order coloumn wise

a=np.array([[4,5,6,1],[1,2,3,4],[6,7,8,3],[7,6,5,4],[1,3,5,7]])
b=np.sort(a,axis=0)
print(b)


