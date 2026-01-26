import secrets
import random
import string
SPECIAL_CHAR = "!@#$%^&*-="
DEFAULT_LENGTH = 12
def Bool(prompt, default_yes=True):
    ans = input(prompt).strip().lower()
    if ans == "":
        return default_yes
    return ans in ("y", "yes")
def User_Specify():
    length_str = input(f"Password length (default {DEFAULT_LENGTH}): ").strip()
    try:
        length = int(length_str) if length_str else DEFAULT_LENGTH
    except ValueError:
        print("Invalid length. Using default.")
        length = DEFAULT_LENGTH
    use_lower = Bool("Include lowercase letters? [yes/no]: ")
    use_upper = Bool("Include uppercase letters? [yes/no]: ")
    use_digits = Bool("Include digits? [Y/n]: ")
    use_special = Bool("Include special characters? [yes/no]: ")
    return length, use_lower, use_upper, use_digits, use_special
def generate_password(length, use_lower, use_upper, use_digits, use_special):
    groups = []
    if use_lower:
        groups.append(string.ascii_lowercase)
    if use_upper:
        groups.append(string.ascii_uppercase)
    if use_digits:
        groups.append(string.digits)
    if use_special:
        groups.append(SPECIAL_CHAR)
    if not groups:
        raise ValueError("You must enable at least one character type.")
    if length < len(groups):
        raise ValueError(f"Length must be at least {len(groups)} to include all selected types.")
    combined = ""
    for g in groups:
        combined += g
    pwd_chars = []
    for g in groups:
        pwd_chars.append(secrets.choice(g))
    remaining = length - len(pwd_chars)
    for _ in range(remaining):
        pwd_chars.append(secrets.choice(combined))
    random.shuffle(pwd_chars)
    pwd = ""
    for ch in pwd_chars:
        pwd += ch
    return pwd
def main():
    while True:
        print("\n1. Generate password")
        print("2. Exit")
        choice = input("Choice: ").strip()
        if choice == "2":
            break
        if choice != "1":
            print("Invalid choice")
            continue
        length, use_lower, use_upper, use_digits, use_special = User_Specify()
        try:
            pwd = generate_password(length, use_lower, use_upper, use_digits, use_special)
        except ValueError as EE:
            print(EE)
            continue
        print("Generated:", pwd)
while True:
    main()
