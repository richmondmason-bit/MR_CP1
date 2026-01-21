import random
import string
alphabet = "abcdefghijklmnopqrstuvwxyz"
digits = "123456789"
length = 12
special_char = "!@#$%^&*-="
def validate_password(pwd: str) -> bool:
    if len(pwd) < length:
        return False
    if not any(c.islower() for c in pwd):
        return False
    if not any(c.isupper() for c in pwd):
        return False
    if not any(c.isdigit() for c in pwd):
        return False
    if not any(c in special_char for c in pwd):
        return False
    return True
def generate_password(length: int = length):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + special_char
    pwd = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(special_char),
    ]
    pwd += [random.choice(chars) for _ in range(length - 4)]
    random.shuffle(pwd)
    return "".join(pwd)
def main():
    while True:
        print("1. Generate password")
        print("2. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            pwd = generate_password()
            print("Generated:", pwd)
        elif choice == "2":
            break
        else:
            print("Invalid choice")
while True:
    main()
