#-------------------two sum ----------------


lst=[1,2,3,4,5,6,7,8,9,10]
tar =6

for i in range(len(lst)):

    for j in range(len(lst)):
        if lst[i] == lst[j]:
            continue
        if lst[i] + lst[j] == tar:
            print(lst[i],lst[j])




