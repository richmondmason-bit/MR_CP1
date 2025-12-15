import turtle, math, random, time

W, H = 800, 600
FPS = 60

PLAYER_SPEED = 260
BULLET_SPEED = 650
ENEMY_SPEED = 90

PLAYER_R = 14
ENEMY_R = 14

screen = turtle.Screen()
screen.setup(W, H)
screen.bgcolor("black")
screen.title("Turtle Shooter – Stable Core")
screen.tracer(0, 0)

def make(shape="circle", color="white", size=1, hide=True):
    t = turtle.Turtle(shape)
    t.color(color)
    t.penup()
    t.speed(0)
    if size != 1:
        t.shapesize(size, size)
    if hide:
        t.hideturtle()
    return t

player = make("triangle", "cyan", 1, False)
player.setheading(90)
px, py = 0.0, 0.0
health = 100
score = 0

hud = make(hide=False)

keys = {"w":0,"a":0,"s":0,"d":0}
mouse = (0,0)
shooting = False

bullets = []
enemies = []

last_shot = 0
SHOT_COOLDOWN = 0.18

def spawn_enemy():
    side = random.choice("tblr")
    if side == "t": x,y = random.randint(-W//2,W//2), H//2+30
    if side == "b": x,y = random.randint(-W//2,W//2), -H//2-30
    if side == "l": x,y = -W//2-30, random.randint(-H//2,H//2)
    if side == "r": x,y = W//2+30, random.randint(-H//2,H//2)

    t = make("circle", "orange", 1, False)
    t.goto(x,y)
    enemies.append([t, x, y, 50])

def fire():
    global last_shot
    now = time.time()
    if now - last_shot < SHOT_COOLDOWN:
        return
    last_shot = now

    mx, my = mouse
    mx -= W/2
    my = H/2 - my
    dx, dy = mx-px, my-py
    d = math.hypot(dx, dy)
    if d == 0: return
    dx, dy = dx/d, dy/d

    t = make("circle","yellow",0.25,False)
    t.goto(px,py)
    bullets.append([t, px, py, dx*BULLET_SPEED, dy*BULLET_SPEED])

def update(dt):
    global px, py, health, score

    if keys["w"]: py += PLAYER_SPEED*dt
    if keys["s"]: py -= PLAYER_SPEED*dt
    if keys["a"]: px -= PLAYER_SPEED*dt
    if keys["d"]: px += PLAYER_SPEED*dt

    px = max(-W/2+15, min(W/2-15, px))
    py = max(-H/2+15, min(H/2-15, py))

    mx,my = mouse
    mx -= W/2
    my = H/2 - my
    player.setheading(math.degrees(math.atan2(my-py,mx-px))-90)
    player.goto(px,py)

    if shooting:
        fire()

    for b in bullets[:]:
        b[1]+=b[3]*dt
        b[2]+=b[4]*dt
        b[0].goto(b[1],b[2])
        if abs(b[1])>W/2+40 or abs(b[2])>H/2+40:
            b[0].hideturtle()
            bullets.remove(b)

    for e in enemies[:]:
        dx, dy = px-e[1], py-e[2]
        d = math.hypot(dx,dy)
        if d>0:
            e[1]+=dx/d*ENEMY_SPEED*dt
            e[2]+=dy/d*ENEMY_SPEED*dt
        e[0].goto(e[1],e[2])

        if math.hypot(e[1]-px,e[2]-py)<PLAYER_R+ENEMY_R:
            health -= 30*dt
            if health<=0:
                game_over()

    for b in bullets[:]:
        for e in enemies[:]:
            if math.hypot(b[1]-e[1],b[2]-e[2])<ENEMY_R:
                e[3]-=25
                b[0].hideturtle()
                bullets.remove(b)
                if e[3]<=0:
                    e[0].hideturtle()
                    enemies.remove(e)
                    score+=10
                break

def draw():
    hud.clear()
    hud.goto(-W/2+10,H/2-30)
    hud.write(f"HP:{int(health)}  Score:{score}",font=("Arial",14,"normal"))
    screen.update()

def game_over():
    hud.goto(0,0)
    hud.color("red")
    hud.write("GAME OVER",align="center",font=("Arial",36,"bold"))
    screen.update()
    time.sleep(2)
    raise SystemExit

def loop():
    update(1/FPS)
    draw()
    screen.ontimer(loop,int(1000/FPS))

def kd(k): keys[k]=1
def ku(k): keys[k]=0

screen.listen()
for k in "wasd":
    screen.onkeypress(lambda k=k:kd(k),k)
    screen.onkeyrelease(lambda k=k:ku(k),k)

cv = screen.getcanvas()
cv.bind("<ButtonPress-1>",lambda e:globals().__setitem__("shooting",True))
cv.bind("<ButtonRelease-1>",lambda e:globals().__setitem__("shooting",False))
cv.bind("<Motion>",lambda e:globals().__setitem__("mouse",(screen.cv.canvasx(e.x),screen.cv.canvasy(e.y))))

for _ in range(6):
    spawn_enemy()

loop()
screen.mainloop()
