
#Airport


weight = float(input("Enter Weight (kg): "))

if weight > 40:
    print("Not Allowed")
elif weight >= 26:
    print("Heavy Baggage")
elif weight >= 16:
    print("Extra Charge")
elif weight >= 1:
    print("Allowed")
else:
    print("No Luggage")