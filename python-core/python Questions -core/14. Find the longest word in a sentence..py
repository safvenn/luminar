string='safvan was a police officer'

lar=0
word=''
lst=[i for i in string.split()]

for i in lst:
    if len(i) > lar:
        lar=len(i)
        word=i

print(word)