lst =[10,15,20,20,55,50,10,14,20,60]
lst1=[]


for char in lst:
    if char not in lst1:
        lst1.append(char)

lst1.sort()

print(lst1)