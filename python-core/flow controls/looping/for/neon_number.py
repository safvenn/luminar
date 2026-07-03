num = int(input("Entera a number: "))
sum =0
sqr = num*num

digit = 0
while sqr>0:
    digit = sqr%10
    sum+=digit
    sqr = sqr//10

if sum == num:
    print("Neon Number")
else:
    print("Not a Neon Number")
    
    
    