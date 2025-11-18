#  Turtle Race Game
# Pseudocode:
# 1. Setup the screen and create turtles with different colors.
# 2. Draw a finish line.
# 3. Move turtles forward randomly in a loop until one crosses the finish line.
# 4. Display which turtle won.
import turtle
import random
screen = turtle.Screen()
screen.title("Turtle Race!")
screen.bgcolor("lightgreen")
screen.setup(width=600, height=400)


finish_line = 200  # must be defined before using it
line = turtle.Turtle()
line.hideturtle()
line.penup()
line.goto(finish_line, 150)
line.pendown()
line.right(90)
line.forward(300)
winner = None
colors = ["red", "green", "orange", "blue", "purple"]
racers = []

for i, color in enumerate(colors):
    t = turtle.Turtle(shape="turtle")
    t.color(color)
    t.penup()
    t.goto(-250, 100 - i * 50)
    racers.append(t)
try:
    while not winner:
        for racer in racers:
            racer.forward(random.randint(1, 10))
            if racer.xcor() >= finish_line:
                winner = racer.pencolor()
                break
except turtle.Terminator:
    print("Turtle window closed.")
    exit()
if winner:
    for racer in racers:
        racer.hideturtle()

    message = turtle.Turtle()
    message.hideturtle()
    message.color("black")
    message.penup()
    message.goto(0, 0)
    message.write(f"{winner.title()} Turtle Wins!", align="center", font=("Arial", 24, "bold"))

turtle.done()
