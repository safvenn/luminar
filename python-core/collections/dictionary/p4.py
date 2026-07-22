sen='apple banana apple grapes banana'


word = sen.split()
# print(word)
dic={}
for i in word:
    if i in dic:
        dic[i]+=1
    else:
        dic[i]=1
print(dic)