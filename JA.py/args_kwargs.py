import random
import shutil
import sys
import time

# ----- COLORS -----
GREEN = "\033[38;5;46m"
BRIGHT = "\033[1m"
DIM_GREEN = "\033[38;5;28m"
RESET = "\033[0m"

# ----- TERMINAL SIZE -----
columns, rows = shutil.get_terminal_size()
columns = min(columns, 80)
rows = min(rows, 24)

# ----- CHARSET -----
charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*"

# ----- SIMPLE MATRIX RAIN -----
def simple_rain(duration=3, density=0.4):
    """
    Smooth Matrix rain effect for a few seconds.
    """
    end_time = time.time() + duration
    while time.time() < end_time:
        for _ in range(int(columns * density)):
            x = random.randint(0, columns - 1)
            y = random.randint(0, rows - 3)  # reserve bottom line
            char = random.choice(charset)
            sys.stdout.write(f"\033[{y+1};{x+1}H{GREEN}{BRIGHT}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(0.05)

def matrix_print(text, speed=0.05):
    """
    Prints any text in Matrix style at the bottom line.
    """
    display = [" " for _ in text]
    for i, c in enumerate(text):
        display[i] = c
        sys.stdout.write(f"\033[{rows};0H{GREEN}{BRIGHT}{''.join(display)}{RESET}")
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write("\n")
    sys.stdout.flush()

# ----- CINEMATIC INTRO -----
def cinematic_intro():
    """
    Plays a short smooth rain intro, then prints messages at the bottom.
    """
    simple_rain(duration=3)
    matrix_print("SYSTEM BOOTING")
    time.sleep(0.3)
    matrix_print("WELCOME USER")
    time.sleep(0.3)
    matrix_print("MATRIX SIMULATION STARTED")
    time.sleep(0.3)

# ----- MAIN PROGRAM -----
def main():
    cinematic_intro()

    # Modular: any text can now be printed in Matrix style
    while True:
        user_input = input("TYPE ANYTHING: ")
        if user_input.strip() == "":
            continue
        matrix_print(user_input.upper())

# ----- ENTRY POINT -----
if __name__ == "__main__":
    main()
