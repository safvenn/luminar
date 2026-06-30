
print("Enter Date of birth \n")

b_day=int(input("enter birth day: "))
b_month=int(input("enter birth month: "))
b_year=int(input("enter birth year: "))
print("Eneter current Date \n")
c_day=int(input("enter current day: "))
c_month=int(input("enter current month: "))
c_year=int(input("enter current year: "))


age=0


if c_year>b_year:
    
    if b_day<=c_day :
        if b_month <= c_month:
           age=c_year-b_year
        else:
            age=c_year-b_year -1
        
else:
    print("Invalid")



print(age)
