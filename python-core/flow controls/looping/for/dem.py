# n=100
# n2=500
# lar =0
# for i in range(n,n2+1):
#     num =i
#     sum=0
#     while num > 0:
#        digit = num % 10
#        sum+=digit ** 3
       
#        num//=10
#     if sum == i:
#        lar=i
# print(lar)

# n=20
# twin=2
# for i in range(2,n+1):
    
#     prime=1
  
#     for j in range(2,i): #3 #5
#         if i % j == 0:
#             prime=0
#             break
#     if prime == 1: #3 #5
        
#         if twin - i == -2: #2-3 == -1, 3-5 == -2
#             print(twin,i)
#         twin=i #3 
        
        
        
        
for i in range(1,5):
    for j in range(i,i+4):
        print(j,end="")
    print()