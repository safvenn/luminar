#1 to 15 'small'
#16 to 35 'medium'
#36 to 50 'large'



lst=[(i,'small') if i <=15 else (i,'medium') if i <= 35 else (i,'large') for i in range(1,51)]


print(lst)