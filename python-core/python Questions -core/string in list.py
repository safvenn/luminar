# 3. find  the longest occurring word  in the list
#    lst=['apple' , 'orange' , 'apple' , 'grapes' , 'apple', 'banana']   --- o/p  will be apple  (repeated the most)


lst=['apple' , 'orange' , 'apple' , 'grapes' , 'apple', 'banana']
dct={}
for i in lst:
    if i not in dct:
        dct[i]=1
    else:
        dct[i]+=1
max_key=max(dct,key=dct.get)
print(max_key)