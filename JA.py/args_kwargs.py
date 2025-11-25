import random
import shutil
import time
import os
columns, rows = shutil.get_terminal_size()
drops = [random.uniform(-rows, 0) for _ in range(columns)]
speeds = [random.uniform(0.3, 1.2) for _ in range(columns)]
trail_lengths = [random.randint(5, 15) for _ in range(columns)]
chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
color_shades = [
    '\033[38;5;46m',  
    '\033[38;5;34m',  
    '\033[38;5;28m',  
    '\033[38;5;22m',  
    '\033[38;5;22m']
RESET = '\033[0m'
last_chars = [[random.choice(chars) for _ in range(columns)] for _ in range(rows)]
try:
    while True:
        print("\033[2J\033[H", end="")  
        for y in range(rows):
            line = ""
            for x in range(columns):
                drop_pos = int(drops[x])
                trail_len = trail_lengths[x]

                if drop_pos >= y and drop_pos - trail_len < y:
                    distance = drop_pos - y
                    color_index = min(distance, len(color_shades) - 1)
                    if random.random() < 0.2:
                        last_chars[y][x] = random.choice(chars)
                    char = last_chars[y][x]
                    if distance != 0 and random.random() < 0.05:
                        char = " "
                    line += color_shades[color_index] + char + RESET
                else:
                    line += " "
            print(line)
        for i in range(columns):
            drops[i] += speeds[i]
            speeds[i] += random.uniform(-0.1, 0.1)
            speeds[i] = max(0.2, min(speeds[i], 1.5))
            if drops[i] - trail_lengths[i] > rows:
                drops[i] = random.uniform(-5, 0)
                speeds[i] = random.uniform(0.3, 1.2)
                trail_lengths[i] = random.randint(5, 15)
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\nMatrix stopped.")
