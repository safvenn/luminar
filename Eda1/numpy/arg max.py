import numpy as np

#Higest value index

# a=np.array([6,5,6,8,6,4,3])
#
# b=np.argmax(a)
#
# print(b)


#TWO Diamention arg Max()-------------------------------
a=np.array([[4,5,6,1],[1,2,3,4],[6,7,8,3],[7,6,5,4],[1,3,5,7]])

b=np.argmax(a)
print(b)

print('*'*100)

# output
# 10 = bcoz 8 is in 10 th index


#arg max on row wise

b=np.argmax(a,axis=0)
print(b)

print('*'*100)
#arg max on column wise

b=np.argmax(a,axis=1)
print(b)