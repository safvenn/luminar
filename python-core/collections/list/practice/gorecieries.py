# 4. Grocery List 🥦

# Given:
# groceries = ["milk", "bread", "eggs"]

# Steps:

# Add 3 more items: "butter", "rice", "tea".

# Remove one bought item "bread".

# Show final list.


# Expected Output:

# Final Grocery List: ['milk', 'eggs', 'butter', 'rice', 'tea']


# ---
groceries = ["milk", "bread", "eggs"]

groceries.extend(["butter", "rice", "tea"])
print(groceries)
brount= input("Eneter brougt item: ")
groceries.remove(brount)
print(groceries)