# one dimentionn max

import numpy as np
# a=np.array([6,5,6,8,6,4,3])
#
# m=np.max(a)
# print(m)


#two dimwntion -----------------------------------------------------

# a=np.array([[4,5,6,1],[1,2,3,4],[6,7,8,3],[7,6,5,4],[1,3,5,7]])
# m=np.max(a)
# print(m)


# axis wise higest value

a=np.array([[4,5,6,1],[1,2,3,4],[6,7,8,3],[7,6,5,4],[1,3,5,7]])
m=np.max(a,axis=1)
print(m)
c=np.max(a,axis=0)
print(c)