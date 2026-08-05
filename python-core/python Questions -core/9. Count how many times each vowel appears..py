string='Education'
dic={}
vowels="aeiou"
for i in string.lower():
    if i in vowels:
        if i in dic:
            dic[i]+=1
        else:
            dic[i]=1


print(dic)