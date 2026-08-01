# Write a Python script to find all Armstrong numbers in the range from 1 to 10000
# and add them to a list. Then, calculate the sum and the average of these Armstrong numbers.
# Additionally, determine and print the smallest and largest Armstrong numbers within this range.
#from unicodedata import digit

lst=[]


for i in range(1,10001):
    total=0
    temp=i
    digits=len(str(i))

    while temp>0:
        data=temp%10
        total+=data**digits
        temp//=10

    if total == i:
        lst.append(i)

print(lst)

print(sum(lst))
print(sum(lst)/len(lst))

print(min(lst))

print(max(lst))