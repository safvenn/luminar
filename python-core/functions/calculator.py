def add(a,b):
    result = a+b
    return result

def sub(a,b):
    result = a-b
    return result

def mult(a,b):
    result = a*b
    return result

def div(a,b):
    result = a/b
    return result

while True:
    print("-----------------------------|""\n1.addition\n-----------------------------|""\n2.substraction\n-----------------------------|""\n3.multiplication\n-----------------------------|""\n4.division\n-----------------------------|""\n0.EXIT\n""-----------------------------|\n")

    choice = int(input("Enter a choice: "))
    if choice == 0:
        break

    num1= int(input("Enter 1st number: "))
    num2= int(input("Enter 2nd number: "))
    
    print("\n")

    if choice==1:
        print(num1,"+",num2,"=",add(num1,num2))
    elif choice==2:
        print(num1,"-",num2,"=",sub(num1,num2))
    elif choice==3:
        print(num1,"*",num2,"=",mult(num1,num2))
    elif choice==4:
        print(num1,"/",num2,"=",div(num1,num2))
    else:
        print("invalid input")