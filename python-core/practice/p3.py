
for i in range(1,100000):
    num=i
    sum = 0



    while num>0:
        digit=num%10
        num=num//10
        fact=1

        for k in range(1,digit+1):
            fact*=k
        sum+=fact

    if sum == i:
        print(i)