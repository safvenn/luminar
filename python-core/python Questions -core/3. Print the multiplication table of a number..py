# 3. Print the multiplication table of a number.
# Input: 7

num=int(input("Enter a number:"))

for i in range(1,10+1):
    print(f"{i} * {num} = {i*num}")