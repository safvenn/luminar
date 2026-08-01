# 3. Write a Python script using list comprehension to perform
# the following tasks on a given list of integers:
# Create a new list containing all integers from the original list
# that are both divisible by 3 and greater than 10.
# Create another list containing the square root of each number from the filtered list.
# Filter this new list to keep only those values that are greater than 5.
# Print the final filtered list of square roots.
# numbers = [4, 9, 12, 15, 22, 30, 36, 45, 50]
numbers=[4,9,12,15,22,30,36,45,50]
newlist=[i for i in numbers if i%3==0 and i>10]
print(newlist)
import math
list=[math.sqrt(i) for i in newlist]
print(list)

list1=[i for i in list if i>5]

print(list1)