




bal = 500

draw=int(input("enter amount to withdrw: "))
while bal>0:
    if bal>=draw:
    
        bal-=draw
        print("BALANCE: ",bal)
        
    else:
        print("Insuffient Balance Try less amount")
    draw=int(input("enter amount to withdrw: "))
print("Balance Exhausted")

