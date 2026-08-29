# 1. collect even numbers
import numpy as np

# a=np.array([6,1,3,4,6,9,3,2,1,5,9,15,20,12,13,18])
# even=a[a%2 == 0]
# print(even)

# 2. 1 to 50 eleemnets metrices, odd number collect, 2d (5,5)

a=np.arange(1,51)

odd=a[a%2!=0]

two_d=odd.reshape(5,5)

print(two_d)
