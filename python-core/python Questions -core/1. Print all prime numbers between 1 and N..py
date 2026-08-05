# 1. Print all prime numbers between 1 and N.
# Sample Input: 20
# Sample Output: 2 3 5 7 11 13 17 19

# num=int(input("Enter a number"))
num=20

for i in range(2,num+1): # 2 , 3 , 4 ,5
    prime = 0
    for j in range(2,i): # 2 ,
        if i % j == 0: #2 % 2 ==0
            prime=1


    if prime == 0:
        print(i,end=' ')