#---------------factotrial _of_numbers--------------------------------



num = int(input("Enter Factorial of number: "))

fact =1
i=1

while i<=num:
    fact*=i
    i+=1
print(f" factorial of {num} is {fact}")