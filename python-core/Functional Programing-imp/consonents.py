string='luminartechnolab'
vowels='aeiou'

lst=[i for i in string  if i.lower() not in vowels]

cou=len(lst)

print(cou)