#


st={1,2,3,5,66,77,74}

#sum
print(sum(st))
#max
print(max(st))
#min
print(min(st))
#len
print(len(st))


#add values

st.add(23)
print(st)

#add multiple values
st.update([21,34,57])
print(st)


#remove an element

st.remove(57)

print(st)

st.pop() #this will remove random value from set
print(st)

st.discard(21)
st.discard(150)

print(st)