num_scores = int(input("Enter the number of scores you want to input: "))
grades = []
total_points = 0  
for i in range(1, num_scores + 1):
    while True:
        try:
            score = float(input(f"Enter score {i} (0-100): "))
            if 0 <= score <= 100:
                break
            else:
                print("Score must be between 0 and 100. Try again.")
        except ValueError:
            print("Invalid input. Enter a number between 0 and 100.")

    if score >= 90:
        letter_grade = "A"
        points = 4.0
    elif score >= 80:
        letter_grade = "B"
        points = 3.0
    elif score >= 70:
        letter_grade = "C"
        points = 2.0
    elif score >= 60:
        letter_grade = "D"
        points = 1.0
    else:
        letter_grade = "F"
        points = 0.0
    
    grades.append((score, letter_grade, points))
    total_points += points
print("\nAll Grades:")
for i, (score, grade, _) in enumerate(grades, start=1):
    print(f"Score {i}: {score} -> Grade: {grade}")
gpa = total_points / num_scores
print(f"\nGPA: {gpa:.2f}")




    