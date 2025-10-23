


password = input("Enter your password: ")


score = 0


if len(password) >= 8:
    score += 1


has_upper = False
for char in password:
    if char.isupper():
        has_upper = True
        break
if has_upper:
    score += 1


has_lower = False
for char in password:
    if char.islower():
        has_lower = True
        break
if has_lower:
    score += 1

has_digit = False
for char in password:
    if char.isdigit():
        has_digit = True
        break
if has_digit:
    score += 1


special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?"
has_special = False
for char in password:
    if char in special_characters:
        has_special = True
        break
if has_special:
    score += 1

if score <= 2:
    strength = "Weak"
elif score == 3:
    strength = "Moderate"
elif score == 4:
    strength = "Strong"
else:
    strength = "Very Strong"


print("Password strength:", strength, f"(Score: {score}/5)")

