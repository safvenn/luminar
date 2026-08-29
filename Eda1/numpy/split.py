import numpy as np

a = np.array([1, 2, 3, 4, 5, 6, 7, 8])

b=np.array_split(a,3)
print(b)


#it splits the arrayy

# output
#
# [array([1, 2, 3]), array([4, 5, 6]), array([7, 8])]