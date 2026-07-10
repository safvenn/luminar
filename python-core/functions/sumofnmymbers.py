


#----------------method1------------------


def sum_n():
    a=int(input('Enter  a number : '))
    sum=0
    for i in range(1,a+1):
        sum+=i
    print(sum)
sum_n()


#----------------method2------------------


def sum_n(a):

    sum=0
    for i in range(1,a+1):
        sum+=i
    print(sum)
sum_n(10)


#----------------method3------------------


def sum_n(a):
    sum=0
    for i in range(1,a+1):
        sum+=i
    print(sum)
    return sum


sum_n(10)


