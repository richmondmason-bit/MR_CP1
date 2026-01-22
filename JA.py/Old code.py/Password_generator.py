
import random
import string
alphabet = "abcdefghijklmnopqrstuvwxyz"
digits = "123456789"
length = 12# Function 1 Set constants: alphabet, digits, default length, special characters.
special_char = "!@#$%^&*-="
def validate_password(pwd: str) -> bool:
    if len(pwd) < length:
#     If length of pwd < required length: return False
        return False
    if not any(c.islower() for c in pwd):
        return False#     If no lowercase letter in pwd: return False
    if not any(c.isupper() for c in pwd):
        return False
#     If no uppercase letter in pwd: return False
    if not any(c.isdigit() for c in pwd):
        return False#     If no digit in pwd: return False
    if not any(c in special_char for c in pwd):
        return False#     If no special character in pwd: return False
    return True
#     Otherwise return True
def generate_password(length: int = length):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + special_char
    pwd = [ #Build a pool of allowed characters (lower, upper, digits, special)
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(special_char),
    ]#Ensure password contains at least one lowercase, one uppercase, one digit, one special
    pwd += [random.choice(chars) for _ in range(length - 4)]
    random.shuffle(pwd)#Fill the remaining characters randomly from the pool
    return "".join(pwd)#     Return the generated password
#     Shuffle the characters and join into a string
def main():
    while True:
        #Loop showing menu: 1. Generate password, 2. Exit
        print("1. Generate password")
#     On choice 1: generate and print password
        print("2. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            pwd = generate_password()
            print("Generated:", pwd)
 #            On choice 2: break loop
        elif choice == "2":
            break
    #    Otherwise: print "Invalid choice"
        else:
            print("Invalid choice")
while True:# Function 5 Run main() in a repeating loop (as in original file)
    main()
