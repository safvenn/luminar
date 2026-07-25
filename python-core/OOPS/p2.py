class Person :
    def setvalue(self,id,fname,lname,age,pro,salary):
        self.id=id
        self.fname=fname
        self.lname=lname
        self.age=age
        self.pro=pro
        self.salary=salary

    def printvalue(self):
        print(self.id,self.fname,self.lname,self.age,self.pro,self.salary)



person1 =Person()

person1.setvalue(101,'safvan','sidheeq',20,'ai engineer',20000)

person1.printvalue()