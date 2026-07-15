##------------------------------Binary Search Algorithm---------------------------------------------------------------



lst =[2,4,3,1,9,8,6,7,5,10]

target = 3
#step 1  -- Sort the array
lst.sort()

#step 2 -- assign two variables(low,upper)

low = 0
upper = len(lst)-1


#assign a flag =0
flag=0



while low <=upper:
    # step 3 -- calculate middle value

    mid = (low + upper) // 2
    if target > lst[mid]:   # target > lst[mid]
        low=mid+1
    elif target<lst[mid]:   # target < lst[mid]
        upper=mid-1
    elif target == lst[mid]:  #target found ---- flag=1
        flag=1
        break
    
if flag == 1:
    print("Found")
else:
    print("Not found")