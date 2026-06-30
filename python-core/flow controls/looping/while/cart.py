

cart =1
total =0
count =0
while cart!=0:
    
        
    p1=int(input(f"Enter Price of Product {count+1} : "))
    
    total+=p1
    count+=1
    
    cart = int(input("press [1] to continue \npress [0] to exit cart....\n"))
    
print("total:",total,"\nNo of Items:",count)
