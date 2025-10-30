import turtle
import random
t = turtle.Turtle()
t.speed(1000)
t.color("black")
def draw_and_move():
    for i in range(100): 
        for _ in range(100):
            t.circle(50)
            t.right(2)  
        t.penup()
        new_x = random.randint(-500, 500)
        new_y = random.randint(-500, 500)
        t.goto(new_x, new_y)
        t.pendown()
draw_and_move()
turtle.done()
