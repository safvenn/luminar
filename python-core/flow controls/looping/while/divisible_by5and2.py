low = int(input("Enter Lower amount: "))
high = int(input("Enter Higher amount: "))


sum = 0

while low<=high:
    if low % 5 == 0 and low % 2 ==0:
        sum+=low
        low+=1
    else:
        low+=1
print(sum)