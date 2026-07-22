dic={
    'id':101,
    'fname':'safvan',
    'lname':'Sidheeq',
    'age':21,
    'profession':'Ai Engineer',
    'location':'Mannarkkad'
}
dic['salary']=15000
dic['lname']='kallayi'
dic.pop('location')
for i in dic:
    print(i,":",dic[i])
dic.clear()
print(dic)