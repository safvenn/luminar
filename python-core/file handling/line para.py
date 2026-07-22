f=open('lines','r')
count=1
long=0
l_line=""
for i in f:
    count+=1
    data=i.upper()
    if len(data) > long:
        long=len(data)
        l_line=data
   # print(data)

print("Number of line count:",count)
print(l_line)
