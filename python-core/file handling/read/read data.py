f= open(r"C:\Users\rehan\OneDrive\Documents\sample4.txt",'r')
# print("Age above 22")
# for i in f:
#     data=i.strip('\n').split(',')
#     age=data[3]
#
#     if age > '22':
#         print(data)


# print("Chennai")
# for i in f:
#     data=i.strip('\n').split(',')
#     age=data[3]
#
#
#     location=data[-1]
#     if location == 'Chennai':
#         print(data[1:4])

for i in f:
    data=i.strip('\n').split(',')
    age=data[3]


    location=data[-1]
    age=data[3]
    if location == 'Chennai' and age>'23' :
        print(data[1:4])


