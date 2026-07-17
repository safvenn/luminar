# 3. Student Marks 📘

# Given:
# marks = [45, 78, 56, 89, 90]

# Steps:

# 1. Sort in ascending order.


# 2. Display highest and lowest.


# 3. Remove lowest and show updated list.



# Expected Output:

# Sorted Marks: [45, 56, 78, 89, 90]
# Highest: 90
# Lowest: 45
# After removing lowest: [56, 78, 89, 90]


# ---

marks = [45, 78, 56, 89, 90]

marks.sort()
print(marks)
print(max(marks))
print(min(marks))
marks.pop(0)
print(marks)
