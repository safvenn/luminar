# 5. Friend List 👯

# Task:
# Keep adding names until "stop" is typed.
# Then check how many times a given name appears and show its position(s).

# Sample Input:

# Enter name: Rahul  
# Enter name: Neha  
# Enter name: Rahul  
# Enter name: Arya  
# Enter name: stop  
# Enter name to search: Rahul

# Expected Output:

# Rahul appears 2 times at positions [0, 2]


# ---
freinds=[]
count=0
pos=[]
while True:
    choice=input("1.Add friends\n2.Search Friends\nEnter input : ")
    if choice=='1':
        while True:
            freind = input("enter name of freind to add(enter stop to stop): ")
            if freind == 'stop':
                break
            freinds.append(freind)
    elif choice == '2':
            freind = input("enter name of freind to search(enter stop to stop): ")
            if freind == 'stop':
                break
            for fr in range(len(freinds)):
                if freinds[fr] == freind:
                    pos.append(fr)
                    count+=1
            print(f"{freind} appers {count} times at {pos}")
                
    else:
        break
    