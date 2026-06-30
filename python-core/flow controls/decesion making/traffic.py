#traffic fine



speeed = int(input("Enter Your speed : "))

if speeed > 120:
    print("License Suspended Recomended")
elif speeed >100:
    print("Fine 2000")
elif speeed >80:
    print("Fine 500")
elif speeed > 60:
    print("Warnning!!!")
else:
    print("Safe Driving")