# largst of three numbers

num1 = int(input("Enter number 1: "))
num2 = int(input("Enter number 2: "))
num3 = int(input("Enter number 3: "))


if num2 < num1 and num1 > num3:
    print(f"{num1} is greater")
elif num2 > num3:
    print(f"{num2} is greater")
else:
    print(f"{num3} is greater")


