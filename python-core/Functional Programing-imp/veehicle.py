
dic={
    'bike':500,'car':2000,'bus':5000,'jeep':2500,'cycle':100,'mini_van':1000
}

lst=[k.upper() for k,v in dic.items() if v>2000]

print(lst)
