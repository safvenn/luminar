
# 1. Shopping Cart 🛒

# Task:
# Start with an empty cart.
# Keep asking the user to add items until they type "done".
# Finally, display all the added items.

# Sample Input:

# Enter item: apple  
# Enter item: milk  
# Enter item: chips  
# Enter item: done

# Expected Output:

# Items in your cart: ['apple', 'milk', 'chips']

cart=[]
item=''
while True:
    item=input('Enter a item and done for complete!..: ')
    if item=="done":
        break
    cart.append(item)
print(cart)
    
    












# 8. Numbers List 🔢

# Given:
# numbers = [10, 20, 30, 40, 50]

# Steps:

# Find sum, largest, smallest.

# Empty the list.


# Expected Output:

# Total: 150
# Largest: 50
# Smallest: 10
# After clearing: []


# ---

# 9. Attendance Sheet 👩‍🏫

# Given:
# students = ["Anu", "Rahul", "Meera", "Arya", "Jithin"]

# Input:

# Absent students: ["Rahul", "Arya"]

# Expected Output:

# Present Students: ['Anu', 'Meera', 'Jithin']


# ---

# 10. Product Inventory 🏪

# Given:
# products = ["pen", "pencil", "eraser", "notebook"]

# Case 1 – Product exists:

# Enter product to search: pencil
# Output: 'pencil' found at position 1

# Case 2 – Product not found:

# Enter product to search: marker
# Output: Product not found. Added to list.
# # Updated Product List: ['pen', 'pencil', 'eraser', 'notebook', 'marker']