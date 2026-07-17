#when ever series increase or decries



lst=[1,3,6,5,3,2,5,6,7,8,7,5,4,8,9,13,15,10,7,5,8,9,10,6]
#[1,6,2,8,4,15,5]
e =[]
# flag=0
# e.append(lst[0])
#for i in range(len(lst)-1):
#     # if i > len(lst)-2:
#     #     break
#     if flag ==0:
#         if lst[i]>lst[i+1]:#6 >5
#             e.append(lst[i]) #6
#             flag=1 #1 dec
#     if flag == 1:
#         if lst[i]<lst[i+1]:
#             e.append(lst[i])
#             flag=0
# print(e)
for i in range(len(lst)-1):
    if lst[i-1]>lst[i]<lst[i+1] or lst[-1]<lst[i]>lst[i+1]:

        print(lst[i])# e.append(lst[i])

