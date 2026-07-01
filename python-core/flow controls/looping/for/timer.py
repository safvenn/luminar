import time

# num = int(input("Enter a number : "))
sec=0
mult =1
x=1
while x!=0:


    mult=1*x
    
    time.sleep(1)
    if mult%60 == 0:
        mult =0
        print(min,"Minutes")
        

    elif mult>=60:
        min=mult//60
        if sec ==59:
            sec=sec//60
        sec+=1
        print(min,"minutes",sec,"second")
        

    else:
        print(mult,"Sec")
    x+=1
    
