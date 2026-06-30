



num = int(input("Enter a number: "))


digit =0
count=0

while num!=0:
    digit = num%10
    if digit % 3 ==0:
        count+=1    
    num=num//10
    
print(count)

