bal = int(input("Add balance: "))

amount = int(input("Enter withdraw amount : "))

if bal == 0:
    print("accout is empty")
elif amount<=0:
    print("inavlid amount")

elif amount > bal :
    print("inssufifcient balance")
elif amount == bal:
    print("Account will be empty!")
else:
    print("transaction sucessfull")