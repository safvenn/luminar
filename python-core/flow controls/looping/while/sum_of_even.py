
num = int(input("Enter a number: "))

tem =0
sum =0

while num!=0:
    temp = num%10
    
    if temp % 2 == 0:
        sum+=temp
    num= num//10
    
print(f"sum of even numbers is {sum}")


    