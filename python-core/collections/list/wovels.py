vowels = "aeiou"

string = "luminar Etechnolab"

empty = []

string = string.lower()

for char in string:
    if char in vowels:
        empty.append(char)


print("count:",len(empty))
print(empty)

