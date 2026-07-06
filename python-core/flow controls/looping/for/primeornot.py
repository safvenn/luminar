low = int(input("Enter a low range: "))
high= int(input("Enter a high range: "))

for j in range(low,high+1):
  flag=1
  if j<=1:
      continue
    

  for i in range(2,j):
    if j % i == 0:
        flag = 0
        break
        
  if flag == 1:
    
    print(j)