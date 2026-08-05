#5. Count how many prime numbers are present between 1 and N.

count=0
n=int(input("Enter a number :"))
for i in range(1,n+1):
    prime=1
    for j in range(2,i):
        if i % j == 0:
            prime=0
    if prime==1:
        count+=1

print(count)