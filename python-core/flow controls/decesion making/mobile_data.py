



gb = float(input("Enter data usage in GB: "))

if gb > 8:
    print("Limit Exceeded")
elif gb >6:
    print("Warning")
elif gb >3:
    print("High Usage")
elif gb > 1:
    print("Normal Usage")
else:
    print("No Usage")