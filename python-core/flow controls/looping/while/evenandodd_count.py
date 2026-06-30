low = int(input("Enter Lower amount: "))
high = int(input("Enter Higher amount: "))

ocount=0
ecount=0
while low<=high:
    if low %2 != 0:
        ocount+=1
        low+=1
    else:
        ecount+=1
        low+=1
print("Count of even numbers:",ecount)
print("Count of odd numbers:",ocount)