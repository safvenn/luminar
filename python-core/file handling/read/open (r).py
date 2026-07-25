#inside from same directory

f=open('../files/demo', 'r')
for i in f:
    print(i)


#from another directory

#demo2 located at C:\Users\rehan\OneDrive\Desktop\luminar\python-core\collections\demo2


m=open(r'/python-core/file handling/demo2', 'r')

for i in m:
    print(i)

