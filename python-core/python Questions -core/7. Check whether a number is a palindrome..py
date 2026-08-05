# 7. Check whether a number is a palindrome.
# Input:121 Output:Palindrome


n=int(input("Enter a number :"))
rev=''
temp=str(n)
while n>0:
    digit=n%10
    rev+=str(digit)
    n//=10


if rev == temp:
    print("Palidrome")
else:
    print("Not a palidrome")