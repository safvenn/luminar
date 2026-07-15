perfect =[]

lst=[]
for i in range(1,10001):
    lst.append(i)

for j in lst:
    sum = 0
    for k in range(1,j):
        if j % k == 0:
            sum+=k
    if sum == j:
        perfect.append(j)


print(perfect)