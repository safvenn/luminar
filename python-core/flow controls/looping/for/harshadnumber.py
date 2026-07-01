num = int(input("enter a number: "))
temp = num
digit = 0

sum =0

harsh = False

for i in range(1,num+1):
    digit = num%10 
    sum+=digit 
    num = num//10
if temp % sum == 0:
    print("Harshad Number")
else:
    print("Not a Harshad Number")
    
    
    