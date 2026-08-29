import  numpy as np



#minimum value index

a=np.array([6,5,6,8,6,4,3])

b=np.argmin(a)

print(b)
print('*'*100)

#TWO Diamention arg Min()-------------------------------
a=np.array([[4,5,6,1],[1,2,3,4],[6,7,8,3],[7,6,5,4],[1,3,5,7]])

b=np.argmin(a)
print(b)

print('*'*100)

# output
# 3


#arg min on row wise

b=np.argmin(a,axis=0)
print(b)

print('*'*100)
#arg min on column wise

b=np.argmin(a,axis=1)
print(b)