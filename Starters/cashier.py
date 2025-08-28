#Mason Richmond 


Writing_assignment1  = float(input("Writing_Grade1: "))
Math_Assignment1     = float(input("Math_Grade1: "))
English_assignment1  = float(input("English_Grade1: "))
Math_homework1       = float(input("Math_Grade2: "))
Writing_assignment2  = float(input("Writing_Grade2: "))
Math_Assignment2     = float(input("Math_Grade3: "))
English_assignment2  = float(input("English_Grade2: "))
Math_homework2       = float(input("Math_Grade4: "))


total_math = Math_Assignment1 + Math_homework1 + Math_Assignment2 + Math_homework2
average_math = total_math / 4


print("Total Math Score:", total_math)
print("Average Math Score:", average_math)
