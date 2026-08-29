import pandas as pd
dic={
    'id':[101,102,103,104,105],
    'name':['salman','adil','basil','jafeer','raju'],
    'age':[21,23,43,19,36],
    'prof':['bigdata','ai','ml','js','python'],
}

a=pd.DataFrame(dic)
print(a)