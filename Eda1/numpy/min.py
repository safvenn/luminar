import numpy as np

a=np.array([6,5,6,8,6,4,3])

m=np.min(a)
print(m)


# two diamention minimum value -----------------------------------------------------

a=np.array([[4,5,6,1],[1,2,3,4],[6,7,8,3],[7,6,5,4],[1,3,5,7]])
m=np.min(a)
print(m)


# axis wise minimum value------------------------------------------------------------

a=np.array([[4,5,6,1],[1,2,3,4],[6,7,8,3],[7,6,5,4],[1,3,5,7]])
m=np.min(a,axis=1)
print(m)
c=np.min(a,axis=0)
print(c)

