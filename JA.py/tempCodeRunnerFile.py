import random
import sys
import time
import os

WIDTH, HEIGHT = 20, 10
snake = [(WIDTH // 2, HEIGHT // 2)]
direction = (0, -1)
food = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))

def print_board():
    os.system('cls' if os.name == 'nt' else 'clear')
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) == snake[0]:
                print('O', end='')
            elif (x, y) in snake:
                print('o', end='')
            elif (x, y) == food:
                print('X', end='')
            else:
                print('.', end='')
        print()
    print('Use WASD keys to move. Ctrl+C to quit.')

def move_snake():
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)
    if head == food:
        return True
    else:
        snake.pop()
        return False

def check_collision():
    head = snake[0]
    if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT):
        return True
    if head in snake[1:]:
        return True
    return False

try:
    while True:
        print_board()
        key = input('Move (WASD): ').lower()
        if key == 'w' and direction != (0, 1):
            direction = (0, -1)
        elif key == 's' and direction != (0, -1):
            direction = (0, 1)
        elif key == 'a' and direction != (1, 0):
            direction = (-1, 0)
        elif key == 'd' and direction != (-1, 0):
            direction = (1, 0)
        ate = move_snake()
        if ate:
            while True:
                new_food = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
                if new_food not in snake:
                    food = new_food
                    break
        if check_collision():
            print_board()
            print('Game Over!')
            break
        time.sleep(0.1)
except KeyboardInterrupt:
    sys.exit()
