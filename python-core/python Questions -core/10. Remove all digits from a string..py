string='Py123thon45'

new=''

for i in string:
    if i.isdigit():
        continue
    new+=i
print(new)