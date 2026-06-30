#------------------------------sum-of-n-numbers------------------------------

num = int(input("Enter number to find sum: "))

sum =0
i=1

while i<=num:
    sum+=i
    i+=1
print(sum,"is sum of",num,"numbers")