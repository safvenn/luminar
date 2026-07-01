low = int(input("Enter Lower limit:  "))
upp = int(input("Enter upper limit: "))

for i in range(low,upp+1):
    if i % 2 ==0 and i % 5 == 0:
        print(i)