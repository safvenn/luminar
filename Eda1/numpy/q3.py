
import numpy as np


a=np.array([[1,2,3],[4,5,6],[7,8,9]])
#conver into 3d dimention

b=a.reshape([1,3,3])
print(b)

print('*'*100)
#conver to 1 daimneton

c=a.reshape([9])



print(c)