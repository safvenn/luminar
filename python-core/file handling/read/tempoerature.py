f=open(r'/python-core/file handling/files/temper.txt', 'r')

dic={}

for i in f:
    data=i.strip("\n").split(',')

    dist=data[0]
    temp=data[1]

    if dist not in dic:
        dic[dist]=temp
    else:
        temp0=dic[dist]
        if temp > temp0:
            dic[dist]=temp

for i,j in dic.items():
    print(i,":",j)