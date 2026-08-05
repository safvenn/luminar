
string= "PyTHon123"

ucount=0
lcount=0
for i in string:
    if i.isupper():
        ucount+=1
    elif i.islower():
        lcount+=1

print(ucount)
print(lcount)