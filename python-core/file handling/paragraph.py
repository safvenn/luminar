f=open('about','r')
for i in f:
    i=i.rstrip(',')

    data=i.split()
print(list(data))
words={}
for j in data:
    if j  in words:
        words[j]+=1
    else:
        words[j]=1

print(words)


