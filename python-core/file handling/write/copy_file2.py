f=open(r'C:\Users\rehan\OneDrive\Desktop\luminar\python-core\file handling\files\fruits','r')

f1=open(r'C:\Users\rehan\OneDrive\Desktop\luminar\python-core\file handling\files\fruits_unique','w')

for i in f:
    fruit=i.strip('\n')
    if fruit != 'apple':
        f1.write(i)
        print(fruit)