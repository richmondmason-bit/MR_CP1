import random
import os
import time
import shutil

# Get terminal size
columns, rows = shutil.get_terminal_size()

# Initialize positions for each column
drops = [random.randint(0, rows) for _ in range(columns)]

try:
    while True:
        # Clear screen slightly (doesn't flicker as much as full clear)
        print("\033[H", end="")  # Move cursor to top-left

        for y in range(rows):
            line = ""
            for x in range(columns):
                # Randomly decide to print a number or space
                if drops[x] == y:
                    line += str(random.randint(0, 9))
                else:
                    line += " "
            print(line)
        
        # Move drops down
        drops = [(d + 1) % rows for d in drops]

        # Speed of the rain
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nMatrix effect stopped.")
