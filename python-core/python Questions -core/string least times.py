# 2. Write a program to find the character that appears the least number of times (excluding spaces).
# # Example: 'mississippi' → 'm' appears once.

st='mississippi'
dic={}
least=0
for i in st:
    if i in dic:
        dic[i]+=1
    else:
        dic[i]=1
    least=dic[i]
min_key=min(dic,key=dic.get)
min_value=min(dic.values())

print(f'{min_key} appears least {min_value} times')
