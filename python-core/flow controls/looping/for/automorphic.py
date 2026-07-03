num=int(input("Enter the number : "))
temp = num
digit=0
count=0
sqr = num*num
w = 1
while num >0: 
    num = num//10 
    w = w*10
    digit= sqr % w

if digit == temp:
    print("Automorphic")
else:
    print("Not Automorphic")