# count vowels
# count consents
# count each word count
# wrd count length above 3 words collect

string='practice lst comprehension problem to drill your head'

vowels="aeiouAEIOU"

cvowel= [ i for i in string if i in vowels]

print(len(cvowel),"vowels")


cconsonents= [ i for i in string if i not in vowels and i != ' ']

print(len(cconsonents),"consonents")

data=string.split()
dct={}

for i in data:
    if i not in dct:
        dct[i]=1
    else:
        dct[i]+=1
print(dct)


space=[i for i in string if i == ' ']
print(len(space),"No of space")

words3 = [i for i in string.split() if len(i)>3]

print(words3)