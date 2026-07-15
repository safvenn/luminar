lst = ["safvan sidheeq","shiyas","rinshad","rishana","nafi"]

logest = ""

for i in lst :
    if len(i) > len(logest):
        logest=i

print(logest)