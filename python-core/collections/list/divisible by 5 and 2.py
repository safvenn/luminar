lst=[]


for i in range(1,31):
    if i % 2 == 0 and i % 5 ==0:
        lst.append(i)
print(lst)
print("sum:",sum(lst))