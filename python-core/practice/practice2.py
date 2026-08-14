arr=[10,3,4,5,6,7,8,9,10]
arr.sort()

search=81
#middle

#(low+upper)//2
low=0
upper=len(arr)-1

        #5


#
flag = 0
while upper>=low:
    mid = (low + upper) // 2
    if search>arr[mid]:
        low=mid+1
    elif search<arr[mid]:
        upper=mid-1
    elif search==arr[mid]:
        print("Element found")
        break


else:
    print("Not Founnd")
