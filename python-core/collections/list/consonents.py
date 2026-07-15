#consonents



vowels = "aeiou"

string = "luminar technolab"

empty = []

string = string.lower()

for char in string:
    if char not in vowels:
        empty.append(char)


print("count:",len(empty))
print(empty)

