num = int(input("Entera a number: "))


sum =0
pro =1
digit =0


while num > 0:
    digit = num%10
    sum+=digit
    pro*=digit
    num=num//10
if sum == pro:
    print("Spy Number")
else:
    print("Not a Spy")
    
    