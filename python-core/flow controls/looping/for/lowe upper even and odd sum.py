low = int(input("Enter Lower Limit: "))
upp = int(input("Enter Upper limit: "))
esum=0
osum=0
for i in range(low,upp+1):
    if i % 2 == 0:
        esum+=i
    else:
        osum+=i
print('Sum of even:',esum)
print('Sum of odd:',osum)