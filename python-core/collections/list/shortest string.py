lst = ["safvan sidheeq","shiyas","rinshad","rishana","nafi"]
short= lst[0]

for i in lst :
    if len(i) < len(short):
        short=i


print(short)