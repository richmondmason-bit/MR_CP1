import pygame, math, random, time, sys, os, json

# ================= CONFIG =================
W, H = 960, 720
FPS = 60

ACC_BASE = 1700
FRICTION = 8
MAX_SPEED = 380

DASH_SPEED = 900
DASH_TIME = 0.12
DASH_CD_BASE = 0.9

PLAYER_R = 14
ENEMY_R = 14

RELOAD_TIME_BASE = 1.2

SAVE_FILE = "save.json"
# =========================================

# ================= GUNS ==================
GUNS = [
    {"name":"Pistol","mag":12,"cd":0.25,"spd":820,"recoil":100,"spread":0,"pellets":1},
    {"name":"SMG","mag":30,"cd":0.08,"spd":900,"recoil":70,"spread":6,"pellets":1},
    {"name":"Shotgun","mag":6,"cd":0.7,"spd":750,"recoil":240,"spread":18,"pellets":6},
]
# =========================================

# ================= PERKS =================
PERKS_COMMON = [
    ("Health +25", "hp"),
    ("Speed +15%", "spd"),
    ("Reload -20%", "reload"),
]
PERKS_RARE = [
    ("Dash CD -30%", "dash"),
    ("Max HP +50", "maxhp"),
]
# =========================================

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("FINAL ROGUELITE SHOOTER")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)
big_font = pygame.font.SysFont("consolas", 32)

# ================= PLAYER =================
px, py = W//2, H//2
pvx = pvy = 0.0

health = 100
max_health = 100

acc_mult = 1.0
reload_mult = 1.0
dash_cd_mult = 1.0

gun_id = 0
gun = GUNS[gun_id]
ammo = gun["mag"]
reloading = False
reload_timer = 0
last_shot = 0

dashing = False
dash_timer = 0
dash_cd = 0

ult_charge = 0
ULT_MAX = 100
# ================= GAME ===================
bullets = []
enemies = []
boss = None

wave = 1
difficulty = 1.0
enemies_left = 0
state = "PLAY"  # PLAY / PERK

score = 0
combo = 1.0
combo_timer = 0

perk_choices = []

# ================= META ===================
if os.path.exists(SAVE_FILE):
    try:
        old_highscore = json.load(open(SAVE_FILE))["highscore"]
    except:
        old_highscore = 0
else:
    old_highscore = 0

# ================= FUNCTIONS =================
def increase_health():
    global health
    health = min(health+25, max_health)

def increase_speed():
    global acc_mult
    acc_mult *= 1.15

def reduce_reload():
    global reload_mult
    reload_mult *= 0.8

def reduce_dash_cd():
    global dash_cd_mult
    dash_cd_mult *= 0.7

def increase_max_hp():
    global max_health, health
    max_health += 50
    health = max_health

def spawn_enemy(elite=False):
    side = random.choice("tblr")
    if side=="t": x,y=random.randint(0,W),-30
    if side=="b": x,y=random.randint(0,W),H+30
    if side=="l": x,y=-30,random.randint(0,H)
    if side=="r": x,y=W+30,random.randint(0,H)

    hp = 60 * difficulty
    spd = 110 * difficulty
    if elite:
        hp *= 2
        spd *= 1.4

    ability = random.choice([None,"dash","split","shield"])
    enemies.append({"x":x,"y":y,"hp":hp,"spd":spd,"elite":elite,"ability":ability,"cd":random.uniform(1.5,3),"shield":False})

def spawn_boss():
    return {"x":W//2,"y":-80,"hp":1200*difficulty,"spd":80,"phase":1}

def start_wave():
    global enemies_left, state, boss
    state = "PLAY"
    enemies_left = wave * 6
    enemies.clear()
    bullets.clear()
    boss = None

    if wave % 5 == 0:
        boss = spawn_boss()
    else:
        for _ in range(enemies_left):
            spawn_enemy(random.random()<0.15)

def start_perks():
    global state, perk_choices
    state = "PERK"
    pool = PERKS_RARE if random.random()<0.25 else PERKS_COMMON
    perk_choices = random.sample(pool, 3)

def apply_perk(p):
    if p=="hp": increase_health()
    elif p=="spd": increase_speed()
    elif p=="reload": reduce_reload()
    elif p=="dash": reduce_dash_cd()
    elif p=="maxhp": increase_max_hp()

def fire(mx,my):
    global ammo,last_shot,pvx,pvy
    if reloading or ammo<=0: return
    now=time.time()
    if now-last_shot<gun["cd"]: return
    last_shot=now
    ammo-=1

    dx,dy=mx-px,my-py
    d=math.hypot(dx,dy)
    if d==0: return
    dx,dy=dx/d,dy/d

    pvx -= dx*gun["recoil"]
    pvy -= dy*gun["recoil"]

    for _ in range(gun["pellets"]):
        ang=math.atan2(dy,dx)+math.radians(random.uniform(-gun["spread"],gun["spread"]))
        bullets.append({"x":px,"y":py,"vx":math.cos(ang)*gun["spd"],"vy":math.sin(ang)*gun["spd"],"life":2})

start_wave()

# ================= MAIN LOOP =================
running=True
while running:
    dt = clock.tick(FPS)/1000

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False

        if state=="PLAY":
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_r and not reloading:
                    reloading=True
                    reload_timer=RELOAD_TIME_BASE*reload_mult
                if e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    gun_id = e.key - pygame.K_1
                    gun = GUNS[gun_id]
                    ammo = gun["mag"]
                if e.key==pygame.K_SPACE and dash_cd<=0:
                    mag=math.hypot(pvx,pvy)
                    if mag>0:
                        pvx=pvx/mag*DASH_SPEED
                        pvy=pvy/mag*DASH_SPEED
                        dashing=True
                        dash_timer=DASH_TIME
                        dash_cd=DASH_CD_BASE*dash_cd_mult
                if e.key==pygame.K_q and ult_charge>=ULT_MAX:
                    ult_charge=0
                    for i in range(40):
                        a=random.random()*math.tau
                        bullets.append({"x":px,"y":py,"vx":math.cos(a)*1000,"vy":math.sin(a)*1000,"life":1})

            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                fire(*pygame.mouse.get_pos())

        elif state=="PERK":
            if e.type==pygame.KEYDOWN and e.key in (pygame.K_1,pygame.K_2,pygame.K_3):
                apply_perk(perk_choices[e.key-pygame.K_1][1])
                wave += 1
                difficulty += 0.25
                start_wave()

    if state=="PLAY":
        keys=pygame.key.get_pressed()
        ACC = ACC_BASE*acc_mult
        pvx += (keys[pygame.K_d]-keys[pygame.K_a])*ACC*dt
        pvy += (keys[pygame.K_s]-keys[pygame.K_w])*ACC*dt

        if not dashing:
            pvx -= pvx*FRICTION*dt
            pvy -= pvy*FRICTION*dt

        px+=pvx*dt
        py+=pvy*dt
        px=max(20,min(W-20,px))
        py=max(20,min(H-20,py))

        if dashing:
            dash_timer-=dt
            if dash_timer<=0: dashing=False
        if dash_cd>0: dash_cd-=dt

        if reloading:
            reload_timer-=dt
            if reload_timer<=0:
                ammo=gun["mag"]
                reloading=False

        for b in bullets[:]:
            b["x"]+=b["vx"]*dt
            b["y"]+=b["vy"]*dt
            b["life"]-=dt
            if b["life"]<=0:
                bullets.remove(b)

        for e in enemies[:]:
            dx,dy=px-e["x"],py-e["y"]
            d=math.hypot(dx,dy)
            if d>0:
                e["x"]+=dx/d*e["spd"]*dt
                e["y"]+=dy/d*e["spd"]*dt

            # enemy abilities
            e["cd"] -= dt
            if e["cd"]<0: e["cd"]=0
            if e["ability"]=="dash" and e["cd"]<=0:
                if d>0:
                    e["x"]+=dx/d*120
                    e["y"]+=dy/d*120
                    e["cd"]=2

            if d<PLAYER_R+ENEMY_R:
                health-=60*dt
                if health<=0:
                    running=False

        if boss:
            dx,dy=px-boss["x"],py-boss["y"]
            d=math.hypot(dx,dy)
            if d>0:
                boss["x"]+=dx/d*boss["spd"]*dt
                boss["y"]+=dy/d*boss["spd"]*dt
            if d<40: health-=90*dt
            if random.random()<0.03:
                for i in range(10):
                    a=i*math.tau/10
                    bullets.append({"x":boss["x"],"y":boss["y"],"vx":math.cos(a)*450,"vy":math.sin(a)*450,"life":2})

        for b in bullets[:]:
            for e in enemies[:]:
                if math.hypot(b["x"]-e["x"],b["y"]-e["y"])<ENEMY_R:
                    e["hp"]-=30
                    bullets.remove(b)
                    if e["hp"]<=0:
                        enemies.remove(e)
                        enemies_left-=1
                        combo_timer=2
                        combo=min(combo+0.1,3)
                        score+=int(10*combo)
                        ult_charge=min(ULT_MAX, ult_charge+5)
                        if enemies_left<=0 and not boss:
                            start_perks()
                    break
            if boss and math.hypot(b["x"]-boss["x"],b["y"]-boss["y"])<45:
                boss["hp"]-=25
                bullets.remove(b)
                if boss["hp"]<=0:
                    boss=None
                    score+=500
                    ult_charge=min(ULT_MAX, ult_charge+20)
                    start_perks()

        combo_timer-=dt
        if combo_timer<=0: combo=1.0

    # ================= DRAW =================
    screen.fill((12,12,15))

    if state=="PLAY":
        mx,my=pygame.mouse.get_pos()
        ang=math.atan2(my-py,mx-px)
        pygame.draw.circle(screen,(0,255,255),(int(px),int(py)),PLAYER_R)
        pygame.draw.line(screen,(0,255,255),(px,py),(px+math.cos(ang)*20,py+math.sin(ang)*20),3)

        for b in bullets:
            pygame.draw.circle(screen,(255,255,0),(int(b["x"]),int(b["y"])),3)
        for e in enemies:
            col=(255,50,50) if e["elite"] else (255,120,60)
            pygame.draw.circle(screen,col,(int(e["x"]),int(e["y"])),ENEMY_R+3 if e["elite"] else ENEMY_R)
            if e["shield"]:
                pygame.draw.circle(screen,(80,180,255),(int(e["x"]),int(e["y"])),ENEMY_R+6,2)
        if boss:
            pygame.draw.circle(screen,(180,60,220),(int(boss["x"]),int(boss["y"])),45)

        hud = font.render(
            f"Wave:{wave}  HP:{int(health)}/{max_health}  Gun:{gun['name']}  Ammo:{ammo}/{gun['mag']}  Combo x{combo:.1f}  Score:{score}  ULT:{int(ult_charge)}%",
            True,(220,220,220)
        )
        screen.blit(hud,(10,10))
    else:
        title=big_font.render("CHOOSE A PERK",True,(255,255,255))
        screen.blit(title,(W//2-160,120))
        for i,p in enumerate(perk_choices):
            t=font.render(f"{i+1}. {p[0]}",True,(200,200,200))
            screen.blit(t,(W//2-120,200+i*40))

    pygame.display.flip()

# ================= SAVE ON EXIT =================
try:
    data = {"highscore": max(score, old_highscore)}
    json.dump(data, open(SAVE_FILE,"w"))
except:
    pass

pygame.quit()
sys.exit()
