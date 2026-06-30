#electricity

unit = int(input("enter unit of current"))

free = 100
total = 0
if unit > 200:
    unit = unit-free
    total = (unit-100)*10+500
elif unit > 100:
    unit = unit-free
    total = unit*5

else:
    print("no payment")
print(total)
