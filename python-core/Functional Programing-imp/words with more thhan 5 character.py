#8 lst['apple','orrange','mango','grapes','watermelon','bananna']

#words with more thhan 5 character


lst=['apple','orrange','mango','grapes','watermelon','bananna']


q=list(filter(lambda x: len(x)>5,lst))

print(q)