# # Beginner (10 Questions)
# # 1. Check Positive, Negative or Zero.
# num=12
#
# if num >0:
#     print("Positive")
# else:
#     print("Negative")
#
#
# # 2. Find largest of three numbers without max().
#
# num1=10000
# num2=200
# num3=90
# lar=num1
# if num2 > num1:
#     lar=num2
# if num3 > num2:
#     lar=num3
#
# print(lar)

# 3. Check voting eligibility from age.

# age=18
#
# if age>=18:
#     print("Eligible to vote")
# else:
#     print("Not Eligible")


# 4. Print multiplication table of a number.
# n=3
# for i in range(1,11):
#     print(f"{i}*{n}={i*n}")

# 5. Find sum of digits of a number.
# n=123
# sum=0
# for i in range(len(str(n))):
#     digit=n%10
#     sum+=digit
#     n//=10
#
# print(sum)

    
# 6. Reverse a number.
# n=123
# rev=0
# for i in range(len(str(n))):
#     digit=n%10
#     rev=(rev*10)+digit
#     n//=10
# print(rev)


# 7. Count even and odd numbers in a list.
#
# lst=[1,2,3,4,5,6,7]
#
# even=[i for i in lst if i %2 ==0]
# odd=[i for i in lst if i %2 ==1]
# print(even)
# print(odd)
# 8. Check leap year.

n=2024

if n % 400 ==0:
    print("leap year")
elif n%4==0 and n%100==0:
    print("Leap year")
else:
    print("Not a leap year")


# 9. Count vowels in a string.


# 10. Find largest element in a list.



