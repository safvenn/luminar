from traceback import print_tb

string='propgramming'


dic={}


for i in string:
    if i not in dic:
        dic[i]=1
    else:
        dic[i]+=1

for k,v in dic.items():
    if v==1:
        print(k)
        break


