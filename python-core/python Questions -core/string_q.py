# 1.Write a program to find the character that appears the most number of times in a string.
# Example: 'banana' → 'a' appears 3 times.


st='safvannn'
dic={}
long=0
for i in st:
    if i in dic:
        dic[i]+=1
    else:
        dic[i]=1

# for k,v in dic.items():
#     if v > long:
#         long=v
#         key=k
#
# print(f"{key} appears {long} times")

max_key=max(dic,key=dic.get)
max_value=max(dic.values())

print(f"{max_key} appears {max_value} times")
