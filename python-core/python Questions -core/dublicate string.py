# Check for Duplicate Characters
# 4. Write a program to check whether a string has duplicate characters or not.
# Example: 'unique' → Output: Yes (since 'u' appears more than once)


st='mississippi'
lst=[]
least=0
for i in st:
    if i not in lst:
        print(f"{i} apears more than once")
        lst.append(i)