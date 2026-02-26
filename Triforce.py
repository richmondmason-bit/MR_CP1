import turtle

def midpoint(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

def draw_triangle(t, p1, p2, p3):
    t.penup()
    t.goto(p1)
    t.pendown()
    t.begin_fill()
    t.goto(p1)
    t.goto(p3)
    t.goto(p2)
    t.end_fill()

def sierpinski(t, p1, p2, p3, depth):
    if depth == 0:
        draw_triangle(t, p1, p2, p3)
        return
    m12 = midpoint(p1, p2)
    m23 = midpoint(p2, p3)
    m31 = midpoint(p3, p1)
    sierpinski(t, p1, m12, m31, depth - 1)
    sierpinski(t, m12, p2, m23, depth - 1)
    sierpinski(t, m31, m23, p3, depth - 1)



screen = turtle.Screen()
screen.title("Sierpinski Triangle / Triforce")
screen.bgcolor("black")


depth_input = screen.textinput(
    "Recursion amount",
    "Change the amount of recursion 1-5\nLeave blank for default: 4"
)
if depth_input is None or depth_input.strip() == "":
    depth = 7
else:
    try:
        depth = int(depth_input.strip())
        if depth < 1 or depth > 5:
            depth = 4
    except ValueError:
        depth = 4


tri_input = screen.textinput(
    "Triforce Colors",
    "Enter pen color and fill color separated by a comma (cyan, blue).\nLeave blank for defaults."
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



sierpinski(t, (-250, -200), (0, 250), (250, -200), depth)

screen.update()
screen.tracer(1, 10)   

screen.exitonclick()