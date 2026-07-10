sum=0

prime=1


for i in range(2,100):
    prime1=1
    for k in range(2,i):
        if i % k ==0:
            prime1 =0
            break
    if prime1 == 1:
        temp=i
        sum=0
        while temp>0:
            digit = temp%10
            temp=temp//10
            sum+=digit

        for j in range(2,sum):
            if sum % j == 0:
                prime=0
                break
            prime = 1
        if prime == 1:
                print(i)
