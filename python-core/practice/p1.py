def amstrong(num):
    temp=num
    count=0
    sum=0
    while temp>0:
        digit=temp%10
        temp=temp//10
        count+=1
    temp=num
    for i in range(count):
        digit=temp%10
        temp=temp//10
        sum+=digit**count
    if sum == num:
        print("Amstrong")
    else:
        print("not amstrong")



amstrong(153)
amstrong(24566)

        

