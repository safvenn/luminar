# 2. Find the factorial of a number using a for loop.
# Input: 5 Output: 120


num=int(input("Enetr a number"))
fact=1
for i in range(1,num+1):
    fact*=i

print(fact)