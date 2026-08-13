#even
# lst=[1,2,3,4,5,6,7,8,9,10]
#
# even=list(filter(lambda x: x%2==0,lst))
# print(even)

#square
#
# sqr=list(map(lambda x: x*x,lst))
# print(sqr)
#
# #list upper
#
# lst=['apple','orange','mango','chaya']
#
# upperx=list(map(lambda x:x.upper(),lst))
#
# print(upperx)


#Write a function validate_password(password) that checks whether a password:
# Is at least 8 characters long
#  Contains at least one uppercase letter
#  Contains at least one digit
#  Return True or False.
# Expected Outcome:
#  Input "Test1234" → True
#  Input "test123" → False

# def password_validation(passw):
#     valid=False
#     if len(passw) >= 8:

#         for i in passw:
#             if i.isdigit():
#                 valid=True
#             elif i.isupper():
#                 valid=True
#         print(valid)
#     else:
#         print(valid)



# intp=input('Enter a passwrd: ')
# password_validation(intp)


#dict
# Given two dictionaries:
#  dict1 = {"a": 100, "b": 200, "c": 300}
#  dict2 = {"a": 300, "b": 100, "d": 400}
#  Merge both dictionaries. If a key exists in both, sum their values.
#  Expected output: {"a": 400, "b": 300, "c": 300, "d": 400}
#
# new={}
# dict1 = {"a": 100, "b": 200, "c": 300}
# dict2 = {"a": 300, "b": 100, "d": 400}
#
# for i in dict1:
#     for j in dict2:
#         if i == j:
#             new[i]=dict1[i]+dict2[i]
#         else:
#             new[i]=dict1[i]
#             new[j]=dict2[j]
#
# print(new)


#second largest
#
# lst=[]
#
# lar=float("-inf")
# sec=float("-inf")
#
# for i in lst:
#         if i > lar:
#             sec=lar
#             lar=i
#         elif lar>i>sec:
#             sec=i
#
#
#
# print(lar)
# if sec == float("-inf"):
#     print("No second largest element")
# else:
#     print(sec)


#sort list without sort()


# lst=[0,0,0,1,2,3,0,4,5,6]
#
#
# for i in range(len(lst)):
#     if lst[i]!=0:
#         lst.pop(i)
#         lst.insert()
#
#
#
# print(lst)