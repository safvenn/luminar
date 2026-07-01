import time

num = int(input("Enter a number : "))

mult =1
x=1
while x!=0:

    # for i in range(x):
    mult=x*num
    time.sleep(1)
    print(f"{x} * {num} = {mult}")
    x+=1
