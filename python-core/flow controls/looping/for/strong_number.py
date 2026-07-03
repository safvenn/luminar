num = int(input("Enter a number: "))
sum =0
temp = num
digit =0
while num != 0:
    digit = num % 10 #5 4 1
    num = num // 10  # 14, 1
    fact = 1

    for j in range(1,digit+1):#5 4 1

        fact *= j # 120 24 1

    sum+= fact #125+24+1 = 145



if temp == sum:
    print("Strong")
else:
    print("Not a strong")

        
        