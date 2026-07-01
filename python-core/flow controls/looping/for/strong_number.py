num = int(input("Enter a number: "))
sum =0
temp = num
fact = 1
digit =0
for i in range(num+1):
    digit = num % 10
    for j in range(1,digit+1):
        fact *= j
    sum+=fact
    num = num//10
if temp == sum:
    print("Strong")
else:
    print("Not a strong")
        
        
        