#leet

lst =[10,30,15,4,7,14,20]

last1=[]


for i in lst:
    result = sum(lst)-i
    last1.append(result)

print(last1)

