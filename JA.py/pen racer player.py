import turtle
import time

# --- Setup the screen ---
wn = turtle.Screen()
wn.title("Simple Turtle Platformer")
wn.bgcolor("lightblue")
wn.setup(width=800, height=600)
wn.tracer(0)  # Turn off screen updates (manual control)

# --- Player setup ---
player = turtle.Turtle()
player.shape("square")
player.color("red")
player.penup()
player.speed(0)
player.goto(0, -250)
player.dy = 0       # vertical velocity
player.dx = 0       # horizontal speed
player.on_ground = False

# --- Platform setup ---
platforms = []

def create_platform(x, y, width):
    platform = turtle.Turtle()
    platform.shape("square")
    platform.color("green")
    platform.shapesize(stretch_wid=1, stretch_len=width)
    platform.penup()
    platform.goto(x, y)
    platforms.append(platform)

# Ground
create_platform(0, -280, 20)
# Floating platforms
create_platform(-200, -150, 5)
create_platform(150, -50, 5)
create_platform(0, 100, 4)

# --- Controls ---
def go_left():
    player.dx = -4

def go_right():
    player.dx = 4

def stop_move():
    player.dx = 0

def jump():
    if player.on_ground:
        player.dy = 10
        player.on_ground = False

wn.listen()
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeyrelease(stop_move, "a")
wn.onkeyrelease(stop_move, "d")
wn.onkeypress(jump, "w")

# --- Game loop ---
gravity = -0.5

while True:
    wn.update()

    # Apply gravity
    player.dy += gravity
    player.sety(player.ycor() + player.dy)
    player.setx(player.xcor() + player.dx)

    # Collision with floor
    if player.ycor() < -250:
        player.sety(-250)
        player.dy = 0
        player.on_ground = True

    # Check platform collisions
    for p in platforms:
        if (abs(player.xcor() - p.xcor()) < (p.shapesize()[1] * 10)) and \
           (abs(player.ycor() - p.ycor()) < 20) and \
           (player.dy <= 0):
            player.sety(p.ycor() + 20)
            player.dy = 0
            player.on_ground = True
            break
    else:
        player.on_ground = False

    # Small delay
    time.sleep(0.02)
