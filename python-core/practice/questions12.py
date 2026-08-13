#Separate even and odd numbers from a list.

# lst=[1,2,3,4,5,6,7,8]
#
# even=[i  for i in lst if i%2==0]
# odd=[i for i in lst if i%2!=0]
#
#
# print("even",even)
# print("odd",odd)
#

#Find the second largest number in a list.
# sec=0
# lar=0
# lst=[10,8,10]
#
# for i in range(len(lst)):
#     for j in range(1,len(lst)):
#         if  lst[j] > lst[i]:
#             lar=lst[j]
#             sec=lst[i]
# print(sec)
#
# Remove duplicates from a list without using
#
#
# lst=[1,1,2,2,3,3]
#
# lst1=[]
# for i in range(len(lst)):
#     for j in range(len(lst)):
#         if lst[j] in lst1:
#             lst.pop(   j)
#         else:
#             lst1.append(j)
#
#
# print(lst)
#
# #
# for i in range(1,6):
#     for j in range(5,5-i,-1):
#         print(j,end=' ')
#     print()
#

# 5
# 5 4
# 5 4 3
# 5 4 3 2
# 5 4 3 2 1


# lst=[1, 2, 3, 4, 5]
#
# k=2
#
# for _ in range(k):
#     for i in range(len(lst)-1,0,-1):
#         lst[i],lst[i-1]=lst[i-1],lst[i]
#
# # lst= lst[-k:]+lst[:-k]
#
# print(lst)

lst=[5,6,7,20,21,22,23]
lst1=[]


# for i in lst:
#     count = 0
#
#     for j in range(i,i*i):
#         for k in lst:
#             if j != k:
#                 count+=1
#     lst1.append(count)
#
# print(lst1)



# for i in range(1,6):
#     for j in range(1,i):
#         print(j,end=" ")
#     print()
# for i in range(6,1,-1):
#     for j in range(1,i):
#         print(j,end=" ")
#     print()
#
#


# for ik in range(0,6):
#     for jk in range(6-ik):
#         print(" ",end=' ')
#     for k in range(1,ik):
#         print(jk,end=" ")
#     print()
# for i in range(6,1,-1):
#     for k in range(6-i):
#         print(" ",end=" ")
#     for j in range(1,i):
#         print(j,end=" ")
#     print()



