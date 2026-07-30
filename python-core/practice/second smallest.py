# Write a Python script to find the second smallest number in a given list of integers.
# Then, perform the following tasks: Remove all occurrences of the second smallest number from the list Calculate the product of the remaining numbers in the list.
# Sort the modified list in descending order and print it.


lst=[10,15,25,15,30,35,40,40,45,50,55,55,60]

unique =list(set(lst))

unique.sort()

print(unique)

second_smallest=unique[1]
print(second_smallest)

lst1=[]

for i in lst:
    if i != second_smallest:
        lst1.append(i)

print(lst1)
