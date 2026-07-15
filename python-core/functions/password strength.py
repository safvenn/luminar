paswrd = input("enter password: ")
def strengthcheck(paswd):
    strength = 0
    for char in paswrd:
        if char in "1234567890":
            strength +=1
        if char in "!@#$%&*":
         strength+=1
        if paswrd.isupper():
            strength+=1
    sr =""
    if strength == 3:
        print("strong")
    elif strength == 2:
        print("Medium")
    elif strength == 1:
        print("Low")
    else:
        print("Please make password strong")


strengthcheck(paswrd)