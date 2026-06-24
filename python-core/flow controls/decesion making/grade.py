#grade


sub1=int(input("enter mark of sub1: "))
sub2=int(input("enter mark of sub2: "))
sub3=int(input("enter mark of sub3: "))
sub4=int(input("enter mark of sub4: "))



total=sub1+sub2+sub3+sub4


if total >= 180:
    print("A+")
elif total >= 160:
    print("A")
elif total >= 140:
    print("B+")
elif total >= 120:
    print("B")
elif total >= 100:
    print("C+")
else:
    print("failed")
