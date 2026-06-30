


while True:
    user =int(input("1.Attendance\n2.Done\n:"))
    
    if user ==1:
        name = input("Enter Student name: ")
        print(name,"Present")
    elif user == 2:
        break
    else:
        print("Invalid Input")