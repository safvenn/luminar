# 8. Find the sum of odd digits in a number.
# Input:58391 Output:17

sum=0
num=int(input("enter a nuumber: "))
while num > 0:
    dig=num%10
    if dig %2 !=0:
        sum+=dig
    num//=10

print(sum)