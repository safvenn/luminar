priority = int(input("Enter priority number: "))

if priority >=9:
    print("ICU Admmission")
elif priority >=7:
    print("Emergency ward")
elif priority >= 4:
    print("Priority consulatation")
elif priority >=1:
    print("Normal checkup")
else:
    print("No treatment")