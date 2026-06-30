low = int(input("Enter Lower amount: "))
high = int(input("Enter Higher amount: "))


while low<=high:
    if low %2 != 0:
        print(low)
        low+=1
    else:
        low+=1
        