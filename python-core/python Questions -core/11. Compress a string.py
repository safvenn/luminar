# 11. Compress a string (Example: aaabbc -> a3b2c1).


string='aaabbac'

dic={}


for i in string:
    if i not in dic:
        dic[i]=1
    elif i in dic and dic[i]==1:
        dic[i]+=1

for k,v in dic.items():
    print(f"{k}{v}",end='')

# x=''
# count=0
# for i in string:
#     if i == x:
#         x=i
#         count+=1
# print(f"{i}{count}",end='')

