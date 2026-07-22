#create a file and add some numbers into the file
#Read the file using pytthon and add into a list and print


f=open('numbers','r')
num=[]
for i in f:
    num.append(int(i))
    print(i)

print(num)
print(sum(num))