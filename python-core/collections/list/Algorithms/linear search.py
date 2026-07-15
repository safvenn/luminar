#----------------------------linear searching algorithm -------------------------------------------------------------------------



def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

arr = [5, 8, 2, 9, 1]

print(linear_search(arr, 9))






#more time complecity


