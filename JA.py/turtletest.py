from turtle import *


height = 360
width = 360
screen = Screen()
screen.screensize(width, height)


tu = Turtle()
tu.hideturtle()
tu.speed(0)
tu.penup()


def decreasePoint(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


for x in range(width):
    for y in range(height):

        a = decreasePoint(x, 0, width, -2, 2)
        b = decreasePoint(y, 0, height, -2, 2)
        ca = a
        cb = b

        n = 0
        z = 0
        while n < 100:
            aa = a * a - b * b
            bb = 2 * a * b

            a = aa + ca
            b = bb + cb
            n += 1

            if abs(a + b) > 16:
                break
        bright = 'pink'
        if (n == 100):
            bright = 'black'

        tu.goto(x , y)
        tu.pendown()
        tu.dot(4, bright)
        tu.penup()
done()