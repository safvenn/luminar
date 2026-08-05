# 4. Find the sum of all even numbers between two given numbers.
# Input: 10 20 Output: 90


num1=int(input("Enter number1: "))
num2=int(input("Enter number2: "))


lst=[i for i in range(num1,num2+1) if i % 2 ==0]

print(sum(lst))