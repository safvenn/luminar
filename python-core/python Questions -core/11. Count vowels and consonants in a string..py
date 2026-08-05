#11. Count vowels and consonants in a string.


vowels="aeiouAEIOU"

string="Safvan Sidheeq"

lst=[i for i in string if i in vowels]
lst1=[i for i in string.strip() if i not in vowels]
print(len(lst),"vowels")
print(len(lst1),"Consonents")