

user = int(input("Enter 1 to book ticket"))

    
total =10
while user == 1 and total!=0:
        if user ==1:
            print("Ticket conformed...!")
            total-=1
            print("Ticket Left:",total)
            user = int(input("Do you want to book again?"))
        else:
                print("Invalid")
print("Sorry Buss is full...!")