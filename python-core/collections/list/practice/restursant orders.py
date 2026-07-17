# 7. Restaurant Orders 🍔

# Task:
# Take orders continuously.
# When chef completes one, remove it.
# When all done, print message.

# Sample Execution:

# Orders received: ['Burger', 'Pasta', 'Pizza']
# Chef completed: Burger
# Chef completed: Pasta
# Chef completed: Pizza
# All orders served!

# Expected Output:

# All orders served!


# ---
orders=[]
completed=[]
while True:
    order=input('Enter order items: ')
    if order == "stop":
        break

    orders.append(order)

for i in range(len(orders)):
    ready=input("Completed item: ")
    completed.append(ready)
    
    
print("All orders served")
