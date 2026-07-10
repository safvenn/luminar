#--------method 1 ---------------------------

def fact(a):
    fact=1
    
    for i in range(1,a+1):
        fact*=i
    print(fact)

fact(5)


#-------method 2---------------

def fact():
    num=int(input("Enter a number: "))
    fact=1
    
    for i in range(1,num+1):
        fact*=i
    print(fact)

fact()


#-------------method 3-------------------------

def fact(a):
    fact=1
    
    for i in range(1,a+1):
        fact*=i
    return fact

fact(5)
