import turtle

def get_midpoint(point1, point2):
    x = (point1[0] + point2[0]) / 2
    y = (point1[1] + point2[1]) / 2
    return (x, y)

def draw_triangle(t, p1, p2, p3):
    t.penup()
    t.goto(p1)
    t.pendown()
    t.begin_fill()
    t.goto(p2)
    t.goto(p3)
    t.goto(p1)
    t.end_fill()


def sierpinski(t, p1, p2, p3, depth):
    if depth <= 0:
        draw_triangle(t, p1, p2, p3)
        return

    m12 = get_midpoint(p1, p2)
    m23 = get_midpoint(p2, p3)
    m31 = get_midpoint(p3, p1)

    sierpinski(t, p1, m12, m31, depth - 1)
    sierpinski(t, m12, p2, m23, depth - 1)
    sierpinski(t, m31, m23, p3, depth - 1)
user_input_recursion = screen.textinput(
    "Recursion amount",
    "Change the amount of recursion(1-5)\nLeave balck for defaulkts"
)
screen = turtle.Screen()
screen.bgcolor("black")

user_input = screen.textinput(
    "Triforce Colors",
    "Enter pen color and fill color separated by a comma (cyan, blue).\nLeave blank for defaults."
)

if user_input is None or user_input.strip() == "":
    pen_color, fill_color = "cyan", "blue"
else:
    parts = [p.strip() for p in user_input.split(",") if p.strip()]
    if len(parts) == 0:
        pen_color, fill_color = "cyan", "blue"
    elif len(parts) == 1:
        pen_color = parts[0]
        fill_color = parts[0]
    else:
        pen_color, fill_color = parts[0], parts[1]


user_input_background = screen.textinput(
    "Background Colors",
    "Enter Background color and fill color separated by a comma (e.g. cyan, blue).\nLeave blank for defaults."
)

if user_input_background is None or user_input_background.strip() == "":
    screen.bgcolor("black")
    fill_color = "yellow"
else:
    parts_bg = [p.strip() for p in user_input_background.split(",") if p.strip()]
    if len(parts_bg) == 0:
        screen.bgcolor("black")
        fill_color = "yellow"
    elif len(parts_bg) == 1:
        screen.bgcolor(parts_bg[0])
        fill_color = parts_bg[0]
    else:
        screen.bgcolor(parts_bg[0])
        fill_color = parts_bg[1]


my_turtle = turtle.Turtle()
my_turtle.speed(0)
my_turtle.color(pen_color)
my_turtle.fillcolor(fill_color)
my_turtle.hideturtle()

bottom_left = (-250, -200)
top_middle = (0, 250)
bottom_right = (250, -200)


depth_level = 4 
sierpinski(my_turtle, bottom_left, top_middle, bottom_right, depth_level)

screen.exitonclick()