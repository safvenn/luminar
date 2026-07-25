#student
# id,fname,lname,course,sem,college



class Student:
    college='MES'
    def setvalue(self,id,fname,lname,course,sem):
        self.id=id
        self.fname=fname
        self.lname=lname
        self.course=course
        self.sem=sem
    def printvalue(self):
        print(self.id,self.fname,self.lname,self.course,self.sem,Student.college)


student1=Student()

student1.setvalue(101,"safvan",'sidheeq','BCA',6)

student1.printvalue()