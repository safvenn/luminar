def amstrong():
    num =  int(input('Enter a number: '))
    temp=num
    sum=0
    count=len(str(num))
    for i in range(count):
        digit=temp%10
        temp=temp//10
        sum+=digit**count
    if sum==num:
        print("Amstrrong")
    else:
        print("Not an amstrong")


amstrong()