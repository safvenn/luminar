#12. Remove duplicate characters while maintaining order.

string="safvan"

ls=''
for i in string:
    if i not in ls:
        ls+=i

print(ls)
