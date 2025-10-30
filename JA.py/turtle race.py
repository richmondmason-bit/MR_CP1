import turtle
import random
screen = turtle.Screen()
screen.title("Turtle Race!")
screen.bgcolor("lightgreen")
screen.setup(width=600, height=400)
colors = ["red", "green", "orange", "blue", "purple"]
racers = []
for i, color in enumerate(colors):
    t = turtle.Turtle(shape="turtle")
    t.color(color)
    t.penup()
    t.goto(-250, 100 - i * 50)
    racers.append(t)
finish_line = 200
line = turtle.Turtle()
line.hideturtle()
line.penup()
line.goto(finish_line, 150)
line.pendown()
line.right(90)
line.forward(300)
winner = None
while not winner:
    for racer in racers:
        racer.forward(random.randint(1, 10))
        if racer.xcor() >= finish_line:
            winner = racer.pencolor()
            break
for racer in racers:
    racer.hideturtle()

message = turtle.Turtle()
message.hideturtle()
message.color("black")
message.penup()
message.goto(0, 0)
message.write(f"{winner.title()} Turtle Wins!", align="center", font=("Arial", 24, "bold"))
turtle.done()
