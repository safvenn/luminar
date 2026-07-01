#---------------------difference of odd or even-------------------------------
num = int(input("Enter a number: "))

tem =0
esum =0
osum =0

while num!=0:
    temp = num%10
    
    if temp % 2 == 0:
        esum+=temp
    else:
        osum+=temp
    num= num//10
    
print(f"Diffrence {esum-osum}")

    