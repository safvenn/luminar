# 6. Find the reverse of a number using while.
# Input:12345 Output:54321


n=int(input("Enter a number :"))
rev=''
while n>0:
    digit=n%10
    rev+=str(digit)
    n//=10


print(rev)