#parking fee


hour = int(input("enter hour: "))


if hour >=1:
    print("FEE:,20")
elif hour >=3:
    print("FEE:",50)
elif hour >=6:
    print("FEE",100)
elif hour >10:
    print("FEE:",200)
else:
    print("invalid entry")
