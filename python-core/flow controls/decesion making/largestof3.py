#second largest number


num1=int(input("Enter number 1 : "))
num2=int(input("Enter number 2 : "))
num3=int(input("Enter number 3 : "))


# if (num1 > num2 and num1 < num3) or ( num1 < num2 and num1 > num3):
#     print(num1,"is second largest")
# elif (num2>num1 and num2 < num3 ) or ( num2 > num3 and num2 < num1):
#     print(num2,"is second largest")
# else:
#     print(num3,"is second largest")



if num1 > num2 and num1>num3:
    if num2>num3:
        print("number 2 is second largest")
    else:
        print("Number 3 is 2nd largest")
elif num2>num1 and num2>num3:
    if num1>num3:
        print("Number 1 is second largest")
    else:
        print("number 3 is second largestt")
else:
    if num2>num1 :
        print("Number 2 is second largest")
    else :
        print("Number 1 is second largest")
