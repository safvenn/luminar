#attendance


total_attendance = int(input("Enter total attendance: "))
attended = int(input("Enter attended: "))

attendance=(attended/total_attendance)*100

print(attendance,"%")


if attendance>75:
    print("Eligible for Exam")
else:
    print("Not Eligible for Exam")