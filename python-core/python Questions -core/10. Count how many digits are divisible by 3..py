# 10. Count how many digits are divisible by 3.
# Input:123456789 Output:3


count=0
num=int(input("enter a nuumber: "))
while num > 0:
    dig=num%10
    if dig%3 == 0:
        count+=1
    num//=10

print(count)