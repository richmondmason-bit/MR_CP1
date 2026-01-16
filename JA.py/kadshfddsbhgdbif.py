import pygame, sys, random, math

# =====================
# INIT
# =====================
pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Saucy Parkour Deluxe")
clock = pygame.time.Clock()

# =====================
# COLORS
# =====================
WHITE = (240,240,240)
BLUE = (60,160,255)
GRAY = (100,100,100)
GREEN = (60,220,90)
RED = (220,60,60)
PURPLE = (200,0,255)
ORANGE = (255,165,0)
YELLOW = (255,220,0)

# =====================
# PLAYER
# =====================
player = pygame.Rect(100,300,40,60)
vel_x, vel_y = 0.0, 0.0
on_ground = False
touching_wall = False
wall_dir = 0
facing = 1
wall_run_timer = 0
vaulting = False
vault_timer = 0
dash_timer = 0
combo_score = 0

# =====================
# CONSTANTS
# =====================
SPEED = 6
MAX_SPEED = 9
GRAVITY = 0.9
JUMP_BASE = 14
FRICTION = 0.85
AIR_CONTROL = 0.5
GROUND_CONTROL = 1.0
WALL_RUN_MAX = 30
VAULT_TIME = 12
DASH_FORCE = 15
DASH_COOLDOWN = 30
dash_cooldown = 0

# =====================
# STAMINA
# =====================
STAMINA_MAX = 100
stamina = STAMINA_MAX

# =====================
# COYOTE + JUMP BUFFER
# =====================
COYOTE_TIME = 8
coyote_timer = 0
JUMP_BUFFER = 8
jump_buffer_timer = 0

# =====================
# CAMERA
# =====================
camera_x = 0.0
camera_y_offset = 0.0

# =====================
# HAZARD CLASSES
# =====================
class TimedLaser:
    def __init__(self, rect, period=120):
        self.rect = rect
        self.period = period
        self.timer = random.randint(0, period)
    def update(self):
        self.timer = (self.timer + 1) % self.period
    def active(self):
        return self.timer < self.period // 2

class MovingSpike:
    def __init__(self, rect, axis="x"):
        self.rect = rect
        self.axis = axis
        self.origin = rect.topleft
    def update(self):
        offset = math.sin(pygame.time.get_ticks() * 0.004) * 60
        if self.axis=="x": self.rect.x=self.origin[0]+offset
        else: self.rect.y=self.origin[1]+offset

class SharkLaser:
    def __init__(self, rect, path_length=200, speed=2):
        self.rect = rect
        self.origin = rect.topleft
        self.path_length = path_length
        self.speed = speed
        self.direction = 1
    def update(self):
        self.rect.x += self.speed*self.direction
        if abs(self.rect.x - self.origin[0]) > self.path_length:
            self.direction*=-1

class BreakablePlatform:
    def __init__(self, rect):
        self.rect = rect
        self.active = True
        self.timer = 0
    def step_on(self):
        self.active = False
        self.timer = 40  # frames until respawn
    def update(self):
        if not self.active:
            self.timer -= 1
            if self.timer <=0:
                self.active = True

# =====================
# ROOM GENERATION
# =====================
class Room:
    def __init__(self, platforms, hazards, width):
        self.platforms = platforms
        self.hazards = hazards
        self.width = width
        self.start_x = 0

active_rooms = []
platforms = []
hazards = []
breakable_platforms = []
last_room_x = 0

def room_flat(x):
    plats = [pygame.Rect(x,550,800,50)]
    return Room(plats,[],800)

def room_gaps(x):
    plats = [pygame.Rect(x,550,300,50),
             pygame.Rect(x+420,550,300,50),
             pygame.Rect(x+840,550,300,50)]
    return Room(plats,[],1150)

def room_wallrun(x):
    plats = [pygame.Rect(x,550,400,50),
             pygame.Rect(x+460,300,20,250),
             pygame.Rect(x+520,360,120,20),
             pygame.Rect(x+760,460,200,20)]
    return Room(plats,[],1000)

def room_hazard(x):
    plats = [pygame.Rect(x,550,300,50),
             pygame.Rect(x+380,480,220,20)]
    haz = [TimedLaser(pygame.Rect(x+260,360,20,160)),
           MovingSpike(pygame.Rect(x+300,500,60,20),"x"),
           SharkLaser(pygame.Rect(x+400,480,20,40))]
    return Room(plats,haz,600)

def room_secret(x):
    plats = [pygame.Rect(x,550,300,50),
             pygame.Rect(x+400,450,120,20)]
    secret = BreakablePlatform(pygame.Rect(x+250,400,60,10))
    breakable_platforms.append(secret)
    return Room(plats,[],500)

ROOM_POOL = [room_flat, room_gaps, room_wallrun, room_hazard, room_secret]

def generate_rooms(player_x):
    global last_room_x
    SPAWN_AHEAD = 2500
    DESPAWN_BEHIND = 1000

    # remove old rooms
    platforms[:] = [p for p in platforms if p.right>player_x-DESPAWN_BEHIND]
    hazards[:] = [h for h in hazards if hasattr(h,'rect') and h.rect.right>player_x-DESPAWN_BEHIND]
    active_rooms[:] = [r for r in active_rooms if r.start_x + r.width > player_x-DESPAWN_BEHIND]
    breakable_platforms[:] = [bp for bp in breakable_platforms if bp.rect.right>player_x-DESPAWN_BEHIND]

    # generate new rooms
    while last_room_x < player_x + SPAWN_AHEAD:
        room_fn = random.choice(ROOM_POOL)
        room = room_fn(last_room_x)
        for p in room.platforms: platforms.append(p)
        for h in room.hazards: hazards.append(h)
        room.start_x = last_room_x
        active_rooms.append(room)
        last_room_x += room.width

# =====================
# RESPAWN
# =====================
def respawn():
    global vel_x, vel_y, combo_score
    player.topleft = (100,300)
    vel_x = vel_y = 0
    combo_score = 0

# =====================
# MAIN LOOP
# =====================
while True:
    dt = clock.tick(60)
    screen.fill(WHITE)

    jump_pressed = False
    dash_pressed = False
    for e in pygame.event.get():
        if e.type==pygame.QUIT: pygame.quit(); sys.exit()
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_SPACE:
                jump_pressed=True
                jump_buffer_timer=JUMP_BUFFER
            if e.key==pygame.K_LSHIFT and dash_cooldown<=0:
                dash_pressed=True
                dash_cooldown=DASH_COOLDOWN
            if e.key==pygame.K_r: respawn()

    keys = pygame.key.get_pressed()
    generate_rooms(player.x)

    # STAMINA
    if on_ground and abs(vel_x)<1 and not vaulting:
        stamina=min(STAMINA_MAX,stamina+0.8)

    # COYOTE + JUMP BUFFER
    if on_ground: coyote_timer=COYOTE_TIME
    else: coyote_timer-=1
    jump_buffer_timer-=1

    # HORIZONTAL MOVE
    control = GROUND_CONTROL if on_ground else AIR_CONTROL
    if not vaulting:
        if keys[pygame.K_a]: vel_x-=control
        elif keys[pygame.K_d]: vel_x+=control
        elif on_ground: vel_x*=FRICTION
    vel_x=max(-MAX_SPEED,min(MAX_SPEED,vel_x))

    # JUMP
    if jump_buffer_timer>0 and coyote_timer>0:
        vel_y=-(JUMP_BASE + abs(vel_x)*0.35)
        jump_buffer_timer=0
        coyote_timer=0
        camera_y_offset=-6
        combo_score+=1

    # WALL RUN
    if touching_wall and not on_ground and abs(vel_x)>3 and stamina>0:
        wall_run_timer+=1
        vel_y=min(vel_y,2)
        stamina-=0.6
        if wall_run_timer>WALL_RUN_MAX: touching_wall=False
    else: wall_run_timer=0

    # WALL JUMP
    if jump_pressed and touching_wall and stamina>10:
        vel_y=-JUMP_BASE
        vel_x=-wall_dir*SPEED
        stamina-=12
        combo_score+=1

    # DASH
    if dash_pressed:
        vel_x += DASH_FORCE*facing
        combo_score+=1

    vel_y+=GRAVITY
    dash_cooldown-=1

    # APPLY X
    player.x+=vel_x
    touching_wall=False
    wall_dir=0
    for p in platforms:
        if player.colliderect(p):
            if vel_x>0: player.right=p.left; touching_wall=True; wall_dir=1
            elif vel_x<0: player.left=p.right; touching_wall=True; wall_dir=-1

    # APPLY Y
    player.y+=vel_y
    on_ground=False
    for p in platforms:
        if player.colliderect(p):
            if vel_y>0: player.bottom=p.top; vel_y=0; on_ground=True
            elif vel_y<0: player.top=p.bottom; vel_y=0

    # VAULT
    if not vaulting and on_ground and stamina>15:
        for p in platforms:
            if abs(player.right-p.left)<8 or abs(player.left-p.right)<8:
                if p.top<player.bottom<p.top+18 and abs(vel_x)>4:
                    vaulting=True; vault_timer=VAULT_TIME; vel_y=-8; stamina-=15; vel_x*=1.08; break
    if vaulting:
        vault_timer-=1
        vel_y=-4
        if vault_timer<=0: vaulting=False

    # UPDATE BREAKABLE PLATFORMS
    for bp in breakable_platforms:
        if player.colliderect(bp.rect) and bp.active:
            bp.step_on()
        bp.update()

    # HAZARD CHECK
    for h in hazards:
        if isinstance(h,(TimedLaser,MovingSpike,SharkLaser)):
            h.update()
            if player.colliderect(h.rect) and (not isinstance(h,TimedLaser) or h.active()):
                respawn()

    # CAMERA
    camera_x+=(player.centerx-WIDTH//2-camera_x)*0.1
    camera_y_offset*=0.9

    # DRAW
    for p in platforms: pygame.draw.rect(screen,GRAY,pygame.Rect(p.x-camera_x,p.y+camera_y_offset,p.width,p.height))
    for bp in breakable_platforms:
        if bp.active: pygame.draw.rect(screen,ORANGE,bp.rect.move(-camera_x,camera_y_offset))
    for h in hazards:
        color=RED
        if isinstance(h,TimedLaser): color=(255,0,0) if h.active() else (120,120,120)
        elif isinstance(h,SharkLaser): color=PURPLE
        elif isinstance(h,MovingSpike): color=(255,60,60)
        pygame.draw.rect(screen,color,h.rect)
    pygame.draw.rect(screen,BLUE,pygame.Rect(player.x-camera_x,player.y+camera_y_offset,player.width,player.height))

    # STAMINA BAR
    pygame.draw.rect(screen,RED,(20,20,200,10))
    pygame.draw.rect(screen,GREEN,(20,20,200*(stamina/STAMINA_MAX),10))

    # COMBO SCORE
    pygame.draw.rect(screen,YELLOW,(20,40,200,10))
    pygame.draw.rect(screen,ORANGE,(20,40,200*min(combo_score/10,1),10))

    pygame.display.update()
