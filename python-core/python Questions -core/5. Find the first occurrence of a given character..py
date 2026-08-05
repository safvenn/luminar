string='programming'
lst=[]
char='r'
for i in string:
    lst.append(i)

for i in range(len(lst)):
    if char == lst[i]:
        print(i)
        break