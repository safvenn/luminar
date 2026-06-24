#bonus amount


year_of_exp = int(input("Enter year of experience: "))
salary = int(input("Enter salary: "))

if year_of_exp >= 5:
    bonus=(salary*5)/100
    print("Bonus: ", bonus)
else:
    print("No bonus")