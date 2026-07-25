f=open(r'/python-core/file handling/files/customer1.txt', 'r')


#age above 60 fname,lname,age,prof

#Doctor prof, Fname,lmname,age

#age below 50 and prof Doctor f,l,age,

#pilot,f,l,age

#india work ,f,l,age,prof

#Each profession count

# each location count
count={}
for i in f:
    data=i.strip('\n').split(",")
    loc=data[-1]
    age=data[4]
    prof=data[-2]

    # age above 60 fname,lname,age,prof
    # if age > '60' :
    #     print(data[1:5])


    # if prof == 'Doctor':
    #     print(data[1:4])

    # age below 50 and prof Doctor f,l,age,

    # if age < '50' and prof =='Doctor':
    #     print(data[1:4])
    #
    # # pilot,f,l,age
    #
    #
    # if prof =="Pilot":
    #     print(data[1:4])
    #
    # # india work ,f,l,age,prof
    #
    # if loc == 'india':
    #     print(data[1:5])

    # Each profession count


    # if prof not in count:
    #     count[prof]=1
    # else:
    #     count[prof]+=1


    if loc not in count:
            count[loc] = 1
    else:
            count[loc] += 1



print(count)



