#set operations

#1.Union
#2.Intersection
#3.Difference

st1={1,2,3,4,5,6,7,8,9,10}
st2={6,7,8,9,10,11,12,13,14,15}

#Union

st3=st1.union(st2)
print(st3)


#intersection

st4=st1.intersection(st2)
print(st4)

#Difference

st5=st1.difference(st2)

st6=st1-st2 #this is same as using difference function

print(st5)
print(st6)