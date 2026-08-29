import pandas as pd

a = [
    [1, 'safvan', 21, 'ai', 10000],
    [2, 'adil', 32, 'ml', 12000],
    [3, 'salman', 20, 'bigdata', 30000],
    [4, 'jafer', 28, 'python', 20000],
    [5, 'rinshad', 45, 'sql', 5000],
    [6, 'rishana', 32, 'acountant', 8000],
    [7, 'sherbi', 19, 'cma', 10000]
]

# print(a)

df=pd.DataFrame(a)
df.columns=['id','name','age','profession','salary']  # TO add coloumn names
# print(df)
# print('*'*100)
# print(df.shape)
# print('*'*100)
# print(df.head(3))
# print('*'*100)
# print(df.tail(1))
# print('*'*100)
# print(df.dtypes)

#Describe ------------------------------------------------------------------------------------------------
#used for detailed details of each elementss in df (only numerical values)

print(df.describe(include='O')) #use include to get details of string


#           name profession
# count        7          7   -count
# unique       7          7   - unique values
# top     safvan         ai   -most repeated values
# freq         1          1    -frequency of repeated values
print('*' * 100)

print(df.describe(include='all')) # to return all dataypes

#               id    name        age profession        salary
# count   7.000000       7   7.000000          7      7.000000
# unique       NaN       7        NaN          7           NaN
# top          NaN  safvan        NaN         ai           NaN
# freq         NaN       1        NaN          1           NaN
# mean    4.000000     NaN  28.142857        NaN  13571.428571
# std     2.160247     NaN   9.263343        NaN   8599.557021
# min     1.000000     NaN  19.000000        NaN   5000.000000
# 25%     2.500000     NaN  20.500000        NaN   9000.000000
# 50%     4.000000     NaN  28.000000        NaN  10000.000000
# 75%     5.500000     NaN  32.000000        NaN  16000.000000
# max     7.000000     NaN  45.000000        NaN  30000.000000


#NaN = is null values (missing values)

print('*'*100)
#How to add new coloumn---------------------------------------------------------------------------------

df['Gender']=['M','M','F','M','F','F','M']
print(df)
print('*'*100)


#drop a coloumn in df----------------------------------------------------------------------------------

df1=df.drop(['profession','age'],axis=1)  #drop multiple coloumns
print(df1)
