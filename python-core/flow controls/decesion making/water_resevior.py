#water





water = float(input("Enter your water level in Percentage: "))

if water > 100:
    print("FLood Alert")
elif water >= 76:
    print("Full Capacity")
elif water >= 51:
    print("Normal Level")
elif water >= 26:
    print("Low level")
elif water >= 1:
    print("Critical level")
else:
    print("Reservoir Empty")
