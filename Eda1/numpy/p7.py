import numpy as  np

a=np.array([[1,2,3,4,7],[4,3,2,8,1],[3,7,4,1,2],[1,6,3,2,4]])


#convert into (5,4)
b =a.reshape([5,4])

print(b)

c=a.reshape([2,10])

print(c)

d=a.reshape([1,5,4])
print(d)

e=a.reshape([20])
print(e)