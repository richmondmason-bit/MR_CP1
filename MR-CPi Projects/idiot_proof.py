#Mason Richmond, idiot proof assignment
name = input("Enter your full name: ")
phone = input("Enter your phone number (10 digits, e.g. 1234567890): ")
gpa = input("Enter your GPA: ")
name = name.title()
phone = phone[0:3] + " " + phone[3:6] + " " + phone[6:10]
gpa = float(gpa)
gpa = round(gpa, 1)
print("\nThe formatted stuff here")
print("Name:", name)
print("Phone:", phone)
print("GPA:", gpa)
