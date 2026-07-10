def prime():
    num = int(input("Enter a number: "))
    prime=1
    for i in range(2,num):
        if num% i == 0:
            prime=0
            break
    if prime == 1:
        print("Prime")
    else:
        print('not a prime')

while True:
  prime()