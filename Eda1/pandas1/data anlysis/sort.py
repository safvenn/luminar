import pandas as pd 

df=pd.read_csv(r'C:\Desktop\luminar\Eda1\pandas1\files\sample4.txt',sep=',',header=None)
df.columns=['id','fname','lname','age','phno','location']

#sort_values(df)

df1=df.sort_values(by='age')






#1> Age Maximum 2 emp fname,lname,age,phno


max_age=df.sort_values(by='age',ascending=False)[['fname','lname','age']].head(2)
print(max_age)


#2 Age minimum 1 emp f,l,age

age_mini=df.sort_values(by='age')[['fname','lname','age']].head(1)
print(age_mini)


#3 chennai work , age mxm 1 emp f,l,age,phno


chenai_wrk=df.loc[df['location'] == 'Chennai'].sort_values(by='age',ascending=False)[['fname','lname','age']].head(1)
print(chenai_wrk)