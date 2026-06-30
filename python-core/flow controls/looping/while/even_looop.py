#-----------------print even numbers-----------------------------



low=int(input("Enter the lower limit: "))
high=int(input("Enter the upper limit: "))



while low<=high:
    if low%2 == 0:
        print(low)
    low+=1


