num = int(input("Entera a number: "))
sum=0
temp=num
digit = 1
count=0

while num>0:
    count+=1 #1
    num = num//10 #

num=temp

for i in range(1,count):
    while num>0:
        digit = num%10 
        num = num//10 
        pro = digit**count
        count-=i 
        sum+=pro 

if sum == temp:
    print("Disarium Number")
else:
    print("Not a Disarium number")
    
    