import numpy as np
# order must be same

a=np.array([[4,5,2],[4,1,2],[7,6,5]])
b=np.array([[3,7,6],[5,6,2],[4,2,3]])
c=np.concatenate([a,b])
print(c)
print('*'*100)
#output

# [[4 5 2]
#  [4 1 2]
#  [7 6 5]
#  [3 7 6]
#  [5 6 2]
#  [4 2 3]]


d=np.concatenate([a,b],axis=1)
print(d)


#axis=1 for combined array


#output

# [[4 5 2 3 7 6]
#  [4 1 2 5 6 2]
#  [7 6 5 4 2 3]]