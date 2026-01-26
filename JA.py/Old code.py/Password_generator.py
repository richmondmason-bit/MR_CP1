import random
import string
SPECIAL_CHAR = "!@#$%^&*-="
DEFAULT_LENGTH = 12
while True:
    print("\n1. Generate password")
    print("2. Exit")
    choice = input("Choice: ").strip()
    if choice == "2":
        break
    if choice != "1":
        print("Invalid choice")
        continue
    length_str = input(f"Password length (default {DEFAULT_LENGTH}): ").strip()
    try:
        length = int(length_str) if length_str else DEFAULT_LENGTH
    except ValueError:
        print("Invalid length. Using default.")
        length = DEFAULT_LENGTH
    answer = input("Include lowercase letters? [yes/no]: ").strip().lower()
    use_lower = (answer == "" or answer in ("y", "yes"))
    answer = input("Include uppercase letters? [yes/no]: ").strip().lower()
    use_upper = (answer == "" or answer in ("y", "yes"))
    answer = input("Include digits? [Y/n]: ").strip().lower()
    use_digits = (answer == "" or answer in ("y", "yes"))
    answer = input("Include special characters? [yes/no]: ").strip().lower()
    use_special = (answer == "" or answer in ("y", "yes"))
    I_am_sigma = []
    if use_lower:
        I_am_sigma.append(string.ascii_lowercase)
    if use_upper:
        I_am_sigma.append(string.ascii_uppercase)
    if use_digits:
        I_am_sigma.append(string.digits)
    if use_special:
        I_am_sigma.append(SPECIAL_CHAR)
    if not I_am_sigma:
        print("You must enable at least one character type.")
        continue
    if length < len(I_am_sigma):
        print(f"Length must be at least {len(I_am_sigma)} to include all selected types.")
        continue
    def pick(pool):
        return random.choice(pool)

    def join_pools(pools):
        s = ""
        for p in pools:
            s += p
        return s

    def gen_password(pools, length):
        chars = []
        for p in pools:
            chars.append(pick(p))      # ensure each selected type appears
        combined = join_pools(pools)
        for _ in range(length - len(chars)):
            chars.append(pick(combined))
        random.shuffle(chars)
        return "".join(chars)

    print("Generated:", gen_password(I_am_sigma, length))
