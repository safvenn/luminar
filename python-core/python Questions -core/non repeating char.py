# 5. Write a program to find the first non-repeating character in a string.
# Example: 'swiss' → Output: 'w'


st='swiss'
dc={}
for i in st:
    if i not in dc:
        dc[i]=1
    else:
        dc[i]+=1

for k,v in dc.items():
    if v == 1:
        print(k)
        break




