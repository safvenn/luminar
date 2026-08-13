# lst=["apple", "banana", "cat"]
#
#
# f=list(map(lambda x: len(x),lst))
#
# print(f)

# lst = [1, 2, 3, 4, 5,9,14]
#
# f=list(filter(lambda x: x%3 ==0 or x%5 ==0,lst))
# print(f)

# lst = [1, 2, 3, 4, 5]
#
# f=list(map(lambda x: x*-1 if x%2==0 else x,lst))
#
# print(f)

# lst = ["python", "java", "sql", "javascript"]
#
# f=list(filter(lambda x: len(x) > 4,lst))
# print(f)


# lst = [[1, 2], [3, 4], [5, 6]]
#
# f=[i[j] for i in lst for j in range(len(lst)-1)]
# print(f)
#
# flag=0
#
# lst=[i for i in range(2,101) if all(i % j != 0 for j in range(2,i))]
#
# print(lst)


# lst = [1, 2, 3, 4, 5]
#
# f=[(i,i*i) for i in lst ]
#
# print(f)

# #
# lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#
# lst=[i*i for i in range(1,len(lst)+1) if i%2==0]
#
# print(lst)
#
#

#
# lst=[]
#
#
# for i in range(1,1001):
#     sumx = 0
#     for j in range(1,i):
#         if i % j ==0:
#             sumx+=j
#     if sumx == i:
#         lst.append(i)
#
# print(sum(lst))
# print(sum(lst)/len(lst))
# print(max(lst))
# print(min(lst))
#

#
# lst = [2, 7, 11, 15,3,6]
# target = 9
#
# for i in range(len(lst)-1):
#     if lst[i]+lst[i+1] == target:
#         print(lst[i],lst[i+1])