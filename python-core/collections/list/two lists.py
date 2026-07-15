even=[]
odd=[]
lst=[]

for i in range(1,101):
    lst.append(i)
    if i % 2 == 0:
        even.append(i)
    else:
        odd.append(i)
print(lst)
print("Even",even)
print("Odd",odd)
print("sum:",sum(lst))
print("even sum:",sum(even))
print("odd sum:",sum(odd))