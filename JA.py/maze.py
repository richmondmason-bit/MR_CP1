import turtle
import random
#this thing sets the screen size so the maze can fit in the window
width = 600
height = 600
screen = turtle.Screen()
#This is the naming of the window and set up of the background
screen.title("Complex Maze Game")
screen.bgcolor("black")
screen.setup(width=width, height=height)
screen.tracer(0)
#This things set the size and placement on the grid for maze genration blocks
rows, cols = 50, 50
cell_size = 20
pen = turtle.Turtle()
pen.shape("square")
pen.color("white")
#this thing is you know the pen that draws stuff
pen.penup()
pen.speed(0)
#this thing makes the cells 
pen.shapesize(stretch_wid=cell_size / 20, stretch_len=cell_size / 20)
#this thing is the player being set up
player = turtle.Turtle()
player.shape("circle")
player.color("cyan")
player.penup()
player.speed(0)
#yippee finally to the tear-causing maze genration
maze = [[1 for _ in range(cols)] for _ in range(rows)]
#the thing above is making the grid
def passages(y, x):
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]#this is where the blocks can be placed relative to each other
    random.shuffle(directions)
    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if 0 < ny < rows - 1 and 0 < nx < cols - 1 and maze[ny][nx] == 1:#checking the rows and blocks intersect to prevent gaps
            maze[y + dy // 2][x + dx // 2] = 0
            maze[ny][nx] = 0
            passages(ny, nx)
maze[1][1] = 0
passages(1, 1)
for _ in range(random.randint(25, 45)):#random block placer on the grid
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
    new_x = player.xcor() + dx * cell_size#checking if the player can go to a free spot and its not a wall
    new_y = player.ycor() + dy * cell_size
    grid_x = int((new_x + cols * cell_size / 2) // cell_size)
    grid_y = int((rows * cell_size / 2 - new_y) // cell_size)
    if 0 <= grid_x < cols and 0 <= grid_y < rows and maze[grid_y][grid_x] == 0:
        player.goto(new_x, new_y)
       #if you hit the red thingie whcih also spawns in one place you it displays win message
        if (grid_y, grid_x) == (rows - 2, cols - 2):
            win_text = turtle.Turtle()
            win_text.hideturtle()
            win_text.color("yellow")
            win_text.write("You reached the end!!", align="center", font=("Arial", 18, "bold"))
            for key in ["w", "a", "s", "d"]:
                screen.onkeypress(None, key)
#the players movement  thingie that makes player actually move across the grid
def up(): move(0, 1)
def down(): move(0, -1)
def left(): move(-1, 0)
def right(): move(1, 0)
screen.listen()
screen.onkeypress(up, "w")
screen.onkeypress(down, "s")
screen.onkeypress(left, "a")
screen.onkeypress(right, "d")
start_y, start_x = 1, 1
screen_x = -cols * cell_size / 2 + start_x * cell_size
screen_y = rows * cell_size / 2 - start_y * cell_size
player.goto(screen_x, screen_y)
draw_maze()
#keeps the window open
screen.update()
turtle.done()
