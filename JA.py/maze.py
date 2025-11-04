import turtle
import random

wn = turtle.Screen()
wn.title("Simple Maze Game")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)  
rows = 10
cols = 10
cell_size = 40
pen = turtle.Turtle()
pen.shape("square")
pen.color("white")
pen.penup()
pen.speed(0)
player = turtle.Turtle()
player.shape("circle")
player.color("cyan")
player.penup()
player.speed(0)
maze = [[1 for _ in range(cols)] for _ in range(rows)]
y, x = 1, 1
maze[y][x] = 0
while (y, x) != (rows - 2, cols - 2):
    if random.choice([True, False]) and x < cols - 2:
        x += 1
    elif y < rows - 2:
        y += 1
    maze[y][x] = 0
for _ in range(rows * cols // 3):
    ry = random.randint(1, rows - 2)
    rx = random.randint(1, cols - 2)
    maze[ry][rx] = 0
def draw_maze():
    pen.clear()
    for y in range(rows):
        for x in range(cols):
            screen_x = -cols * cell_size / 2 + x * cell_size
            screen_y = rows * cell_size / 2 - y * cell_size
            pen.goto(screen_x, screen_y)
            if maze[y][x] == 1:
                pen.color("white")
                pen.stamp()
            elif (y, x) == (1, 1):
                pen.color("lime") 
                pen.stamp()
            elif (y, x) == (rows - 2, cols - 2):
                pen.color("red")   
                pen.stamp()
def move(dx, dy):
    new_x = player.xcor() + dx * cell_size
    new_y = player.ycor() + dy * cell_size
    grid_x = int((new_x + cols * cell_size / 2) // cell_size)
    grid_y = int((rows * cell_size / 2 - new_y) // cell_size)
    if 0 <= grid_x < cols and 0 <= grid_y < rows and maze[grid_y][grid_x] == 0:
        player.goto(new_x, new_y)
        if (grid_y, grid_x) == (rows - 2, cols - 2):
            win_text = turtle.Turtle()
            win_text.hideturtle()
            win_text.color("yellow")
            win_text.write(" You reached the end!! ", align="center", font=("Arial", 16, "bold"))
def up(): move(0, 1)
def down(): move(0, -1)
def left(): move(-1, 0)
def right(): move(1, 0)
wn.listen()
wn.onkeypress(up, "w")
wn.onkeypress(down, "s")
wn.onkeypress(left, "a")
wn.onkeypress(right, "d")
start_x = -cols * cell_size / 2 + cell_size
start_y = rows * cell_size / 2 - 2 * cell_size
player.goto(start_x, start_y)
draw_maze()
while True:
    wn.update()
