# 9. Find the largest digit in a number.
# Input:294816 Output:9

lar=0
num=int(input("enter a nuumber: "))
while num > 0:
    dig=num%10
    if lar<dig:
        lar=dig
    num//=10

print(lar)