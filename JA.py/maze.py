import turtle
import random
wn = turtle.Screen()
wn.title("Simple Maze ")
wn.bgcolor("black")
wn.setup(width=600, height=600)
pen = turtle.Turtle()
pen.shape("square")
pen.color("white")
pen.penup()
pen.speed(0)
maze = []
while turtle.Turtle():
    random.randint(1,11)

num_blocks = 10 # Number of blocks to place
block_size = 30
screen_width = screen.window_width()
screen_height = screen.window_height()

for y in range(num_blocks):
     
     rand_x = random.randint(-screen_width // 2 + block_size // 2, screen_width // 2 - block_size // 2)
     rand_y = random.randint(-screen_height // 2 + block_size // 2, screen_height // 2 - block_size // 2)

   
colors = ["red", "green", "blue", "yellow", "purple", "orange"]
random_color = random.choice(colors)

draw_block(rand_x, rand_y, block_size, random_color)











turtle.done()
