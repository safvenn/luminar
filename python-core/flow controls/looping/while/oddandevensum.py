low = int(input("Enter Lower amount: "))
high = int(input("Enter Higher amount: "))

osum=0
esum=0
while low<=high:
    if low %2 != 0:
        osum+=low
        low+=1
    else:
        esum+=low
        low+=1
print("sum of odd numbers:",osum)
print("Sum of even nunmbers:",esum)