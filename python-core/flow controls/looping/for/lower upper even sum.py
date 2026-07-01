low = int(input("Enter Lower Limit: "))
upp = int(input("Enter Upper limit: "))
sum=0
for i in range(low,upp+1):
    if i % 2 == 0:
        sum+=i
print('Sum',sum)