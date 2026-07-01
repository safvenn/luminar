



num = int(input("Enter a number: "))


digit =0
temp =0
lar =0

while num!=0:
    digit = num%10
    if digit%2==0:
       if lar<digit:
          lar=digit
        
    num = num//10
    
print(f"largest even number is {lar}")

