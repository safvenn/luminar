import pandas as pd 

import os

os.system("cls")

df=pd.read_csv(r'C:\Desktop\luminar\Eda1\pandas1\files\sample4.txt',sep=',',header=None)
df.columns=['id','fname','lname','age','phno','location']



#Aggrigate functions with Group by

#count() and group by


df1=df.groupby('location')['location'].count().sort_values(ascending=False)
print(df1)



df=pd.read_csv(r'C:\Desktop\luminar\Eda1\pandas1\files\customer1.csv')

prof_count= df.groupby('prof')['prof'].count().sort_values(ascending=False)
print(prof_count)

print("*  aggrigate functi - aggrigate functions and group by.py:27"*100)

loc_count=df.groupby('loc')['loc'].count().sort_values(ascending=False)
print(loc_count)

print("* - aggrigate functions and group by.py:32")

#inida work each prof count


ind=df[df['loc']=='india'].groupby('prof')['prof'].count().sort_values(ascending=False)

print(ind)


x='*'*100
print(x)

#max()


maxx=df['age'].max()
print(maxx)

max_group=df.groupby('prof')['age'].max().sort_values(ascending=False)
print(max_group)

print(x)

#min()


min_age=df['age'].min()


min_group=df.groupby('prof')['age'].min().sort_values(ascending=True)

print(min_group)


#sum()






#mean()


# herairchy

# loc group count sort head/tail