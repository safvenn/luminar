# student = {"name": "Safvan", "age": 21, "mark": 85}
#
# student.pop("age")
# print(stude0nt)


# d = {"a": 10, "b": 25, "c": 15, "d": 30}
#
# print(max(d,key=d.get))

# s = "programming"
#
# d={}
#
# for i in s:
#     if i in  d:
#         d[i]+=1
#     else:
#         d[i]=1
#
# print(d)
#
#
# s = "abbccdde"
#
# d={}
# for i in s:
#     if i  in d:
#         d[i]+=1
#     else:
#         d[i]=1
#
# w=''
# for k,v in d.items():
#     if v==1:
#         print(k)
#         break

# lst=[1,1,2,2,3,3,4,5,6]
# d={}
# lst1=[]
# for i in lst:
#     if i in d:
#         d[i]+=1
#     else:
#         d[i]=1
# for k in d:
#     if d[k] == 1:
#         lst1.append(k)
#
# print(lst1)

d1 = {"a": 10, "b": 20}
d2 = {"a": 30, "c": 40}
d3={}

for k,v in d1.items():
    if k in d2:
        d2[k]+=v
    else:
        d2[k]=v
print(d2)
