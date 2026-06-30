#BMI Calculator


weight = float(input("Enter your weight in KG: "))
height = float(input("Enter your height in CM: "))

height = height / 100


bmi = weight / (height**2)


print("Your BMI is: ", round(bmi,2))


if bmi < 18.5:
    print("Underweight")
elif bmi < 25:
    print("Normal")
elif bmi < 30:
    print("Overweight")
else:
    print("obese")



    