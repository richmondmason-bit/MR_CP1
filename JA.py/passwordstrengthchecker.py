# Function to check password strength
def check_password_strength(password):
    score = 0

    # Check length
    if len(password) >= 8:
        score += 1

    # Check for uppercase letters
    has_upper = False
    for char in password:
        if char.isupper():
            has_upper = True
            break
    if has_upper:
        score += 1

    # Check for lowercase letters
    has_lower = False
    for char in password:
        if char.islower():
            has_lower = True
            break
    if has_lower:
        score += 1

    # Check for digits
    has_digit = False
    for char in password:
        if char.isdigit():
            has_digit = True
            break
    if has_digit:
        score += 1

    # Check for special characters
    special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    has_special = False
    for char in password:
        if char in special_characters:
            has_special = True
            break
    if has_special:
        score += 1

    # Determine strength level
    if score <= 2:
        strength = "Weak"
    elif score == 3:
        strength = "Moderate"
    elif score == 4:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return score, strength

if __name__ == "__main__":
    password = input("Enter your password: ")
    score, strength = check_password_strength(password)
    print(f"Password strength: {strength} (Score: {score}/5)")
