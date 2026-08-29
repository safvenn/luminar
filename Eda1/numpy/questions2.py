

import numpy as np

# Create a NumPy array with values [10, 20, 30, 40, 50]

a=np.arange(10,51,10)
print(a)

print('*'*100)
# Create an array of first 10 natural numbers

a=np.arange(1,11)
print(a)

print('*'*100)

# Create an array of all zeros of size 5


a=np.zeros([5],dtype=int)
print(a)

print('*'*100)

# Create an array of all ones of size 8

a=np.ones([8],dtype=int)
print(a)
print('*'*100)
# Create an array from 1 to 20 with step 2

a=np.arange(1,21,2)
print(a)
print('*'*100)


# Find the sum of all elements in an array


a=np.array([6,1,3,4,6,9,3,2,1,5,9,15,20,12,13,18])
print(a.sum())

print('*'*100)
# Find the mean of the array
a=np.array([6,1,3,4,6,9,3,2,1,5,9,15,20,12,13,18])
avg=np.mean(a)
print(avg)
print('*'*100)
# Find the maximum and minimum values

h=np.max(a)
l=np.min(a)
print(h,l)
print('*'*100)


# Multiply all elements by 2

mul=np.multiply(a,2)
print(mul)
print('*'*100)


# Add two arrays element-wise


a=np.array([1,2,3,4,5])
b=np.array([6,7,8,9,10])
merged=np.add(a,b)
print(merged)


print('*'*100)
# Display the first 5 elements of an array

a=np.array([6,1,3,4,6,9,3,2,1,5,9,15,20,12,13,18])

print(a[:5])



print('*'*100)
# Display the last 3 elements

print(a[-3:])

print('*'*100)
# Display elements from index 2 to 7


print(a[2:7])

print('*'*100)
# Reverse an array

print(a[:-1])

print('*'*100)
# Display alternate elements (even index positions)

even=np.where(a%2==0)

print(even)

print('*'*100)



# Create an array of 12 elements and reshape it into 3×4

a=np.array([1,2,3,4,5,6,7,8,9,11,12,13])
re=a.reshape(3,4)
print(re)
print('*'*100)
# Reshape a 1D array into 2D
# Flatten a 2D array into 1D
# Display elements greater than 25
# Display even numbers from an array
# Display elements divisible by 3
# Replace elements greater than 50 with 100
# Find difference between max and min
# Create two arrays and find their dot product
# Check if all elements are positive
# Create identity matrix of size 4