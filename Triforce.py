import turtle

def sierpinski(size, depth):
    if depth == 0:
        t.begin_fill()
        for i in range(3):
            t.forward(size)
            t.left(120)
        t.end_fill()
    else:
        sierpinski(size / 2, depth - 1)
        t.penup()
        t.forward(size / 2)
        t.pendown()
        t.pendown()
        sierpinski(size / 2, depth - 1)
        t.penup()
        t.backward(size / 2)
        t.left(60)
        t.forward(size / 2)
        t.right(60)
        t.pendown()
        sierpinski(size / 2, depth - 1)
        t.penup()
        t.left(60)
        t.backward(size / 2)
        t.right(60)
        t.pendown()

screen = turtle.Screen()
screen.title("Triforce")
screen.bgcolor("black")
thickness = 1
thickness_input = screen.textinput(
    "Pen thickness amount",
    "Change the amount of thickness\nLeave blank for default: 1"
)
if thickness_input is None or thickness_input.strip() == "":
    turtle.pensize(thickness)
else:
    try:
        thickness = int(thickness_input)
        if thickness < 1 or thickness > 100:
            thickness = 1
    except ValueError:
        thickness = 1
    turtle.pensize(thickness)


depth_input = screen.textinput(
    "Recursion amount",
    "Change the amount of recursion\nLeave blank for default: 4"
)
if depth_input is None or depth_input.strip() == "":
    depth = 4
else:
    try:
        depth = int(depth_input.strip())
        if depth < 1 or depth > 5:
            depth = 4
    except ValueError:
        depth = 4

tri_input = screen.textinput(
    "Triforce Colors",
    "Enter pen color and fill color separated by a comma.\nLeave blank for defaults."
)
if tri_input is None or tri_input.strip() == "":
    pen_color, fill_color = "cyan", "blue"
else:
    parts = [p.strip() for p in tri_input.split(",") if p.strip()]
    if len(parts) == 0:
        pen_color, fill_color = "cyan", "blue"
    elif len(parts) == 1:
        pen_color = fill_color = parts[0]
    else:
        pen_color, fill_color = parts[0], parts[1]

bg_input = screen.textinput(
    "Background Colors",
    "Enter Background color and fill color separated by a comma (e.g. black, yellow).\nLeave blank for defaults."
)
if bg_input is None or bg_input.strip() == "":
    screen.bgcolor("black")
    fill_color = "yellow"
else:
    parts = [p.strip() for p in bg_input.split(",") if p.strip()]
    if len(parts) == 0:
        screen.bgcolor("black")
        fill_color = "yellow"
    elif len(parts) == 1:
        screen.bgcolor(parts[0])
        fill_color = parts[0]
    else:
        screen.bgcolor(parts[0])
        fill_color = parts[1]

t = turtle.Turtle()
t.speed(0)
t.pencolor(pen_color)
t.fillcolor(fill_color)


t.penup()
t.goto(-200, -150)
t.pendown()

sierpinski(400, depth)

screen.update()