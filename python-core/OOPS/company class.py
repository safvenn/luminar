class Employee:
    dpt='IT'
    company="EY"
    def setvalue(self,id,fname,lname,age,salary):
        self.id=id
        self.fname=fname
        self.lname=lname
        self.age=age
        self.salary=salary

    def printvalue(self):
        print(self.id,self.fname,self.lname,self.age,Employee.dpt,self.salary,Employee.company)


emp1=Employee()
emp1.setvalue(101,'safvan','k',21,18000)
emp1.printvalue()
emp2=Employee()
emp2.setvalue(102,'salman','nv',21,10000)
emp2.printvalue()
emp3=Employee()
emp3.setvalue(103,'rinshad','p',31,115000)
emp3.printvalue()
emp4=Employee()
emp4.setvalue(104,'jhon','doe',28,25000)
emp4.printvalue()
emp5=Employee()
emp5.setvalue(105,'abid','k',29,15000)
emp5.printvalue()