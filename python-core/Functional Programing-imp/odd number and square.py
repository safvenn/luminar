#filter function


lst=[1,2,3,4,5,6,7,8,9,10]


cb= list(map(lambda x:x*x,lst))
f=list(filter(lambda x: x%2!=0,lst))
print(cb)
print(f)