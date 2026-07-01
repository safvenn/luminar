num = int(input("Enter a Number "))
og = num
sxm =0

for i in range(1,num+1):
    digit = num%10#3 5 1
    digit=digit**3 
    sxm +=digit#27 125  1 = 153
    num=num//10 #15 1 0
if sxm == og:
    print("Amstrong")
else:
    print("Not an Amstrong")
    
    
    