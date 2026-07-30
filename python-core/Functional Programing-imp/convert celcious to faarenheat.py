#4 temp=[0,20,30,40] convert celcious to faarenheat

#fahrenheit = (celsius * 9/5) + 32

temp=[0,20,30,40]
f=list(map(lambda x: (x* 9/5)+32,temp))

print(f)
