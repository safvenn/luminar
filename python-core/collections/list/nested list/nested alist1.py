lst=[
    [101,'safvan','k',21,'ai engineer',14500],
    [102,'rishana','k',22,'ml',25000],
    [103,'adil','m',25,'video editor',5000],
    [104,'shiyas','m',30,'bigdata',50000],

]
# age == 30
# bigdata
#salary below 10000
#bigdata and age above 29
sum=0
for i in lst:
    if i[3]==30:
        print('age == 30')
        print(i[1:4],'\n')
    if i[4] == 'bigdata':
        print("Big data professionals")
        print(i[1:4],'\n')
    # pyrefly: ignore [unsupported-operation]
    if i[5] < 10000:
        print("Salary below 10k")
        print(i[1:4],'\n')
    # pyrefly: ignore [unsupported-operation]
    if i[3] > 29 and i[4] == 'bigdata':
        print("age above 29 and professional is bigdata")
        print(i[1:4])
    # pyrefly: ignore [unsupported-operation]
    sum+=i[-1]


print("sum",sum)
