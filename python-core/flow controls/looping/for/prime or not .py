num = int(input("Enter a number: "))


prime=True
for i in range(2,num):
    if num % i ==0:
        prime = False
        break
        
if prime == True:
    print("prime Number")
else:
    print("Not a Prime")