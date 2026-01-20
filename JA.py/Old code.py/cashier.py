#Mason Richmond 


Writing_assignment1  = float(input("Writing Grade 1: "))
Math_Assignment1     = float(input("Math Grade 1: "))
English_assignment1  = float(input("English Grade 1: "))
Math_homework1       = float(input("Math Grade 2: "))
Writing_assignment2  = float(input("Writing Grade 2: "))
Math_Assignment2     = float(input("Math Grade 3: "))
English_assignment2  = float(input("English Grade 2: "))
Math_homework2       = float(input("Math Grade 4: "))

total_math = Math_Assignment1 + Math_homework1 + Math_Assignment2 + Math_homework2
average_math = total_math / 4


total_writing = Writing_assignment1 + Writing_assignment2
average_writing = total_writing / 2


total_english = English_assignment1 + English_assignment2
average_english = total_english / 2


total_all = total_math + total_writing + total_english
total_grades = 8  
average_all = total_all / total_grades


print("Total Math Score:", total_math)
print("Average Math Score:", average_math)

print("Total Writing Score:", total_writing)
print("Average Writing Score:", average_writing)

print("Total English Score:", total_english)
print("Average English Score:", average_english)

print("Overall Average Score:", round(average_all, 2))
