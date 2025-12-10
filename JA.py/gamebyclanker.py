import turtle, random, time, math, heapq, sys

FPS = 60
FRAME_TIME = 1.0 / FPS
TILE = 40
VIEW_RADIUS = 6
MM_TILE = 6
MAP_W = 41
MAP_H = 25

wn = turtle.Screen()
wn.setup(1200, 900)
wn.title("Advanced Turtle Dungeon")
wn.bgcolor("#000000")
wn.tracer(0)

pen = turtle.Turtle()
pen.hideturtle(); pen.penup(); pen.speed(0)
hud = turtle.Turtle()
hud.hideturtle(); hud.penup(); hud.speed(0)
mini = turtle.Turtle()
mini.hideturtle(); mini.penup(); mini.speed(0)
player_draw = turtle.Turtle()
player_draw.hideturtle(); player_draw.penup(); player_draw.speed(0)
entities_draw = turtle.Turtle()
entities_draw.hideturtle(); entities_draw.penup(); entities_draw.speed(0)
particles_draw = turtle.Turtle()
particles_draw.hideturtle(); particles_draw.penup(); particles_draw.speed(0)

# Procedural dungeon generation (rooms + corridors)
def generate_dungeon(w, h, room_attempts=16):
    grid = [[1 for _ in range(w)] for _ in range(h)]
    rooms = []
    for _ in range(room_attempts):
        rw = random.randint(4, 8)
        rh = random.randint(4, 7)
        rx = random.randint(1, w - rw - 2)
        ry = random.randint(1, h - rh - 2)
        overlap = False
        for (rx2, ry2, rw2, rh2) in rooms:
            if not (rx + rw < rx2 or rx > rx2 + rw2 or ry + rh < ry2 or ry > ry2 + rh2):
                overlap = True; break
        if not overlap:
            rooms.append((rx, ry, rw, rh))
            for yy in range(ry, ry + rh):
                for xx in range(rx, rx + rw):
                    grid[yy][xx] = 0
    # connect rooms with simple corridors (walk between centers)
    for i in range(len(rooms) - 1):
        ax = rooms[i][0] + rooms[i][2] // 2
        ay = rooms[i][1] + rooms[i][3] // 2
        bx = rooms[i + 1][0] + rooms[i + 1][2] // 2
        by = rooms[i + 1][1] + rooms[i + 1][3] // 2
        x, y = ax, ay
        while x != bx:
            grid[y][x] = 0
            x += 1 if bx > x else -1
        while y != by:
            grid[y][x] = 0
            y += 1 if by > y else -1
    # outline walls
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 1:
                # if adjacent floor then keep as wall
                pass
    start_room = rooms[0] if rooms else (w//2, h//2, 3, 3)
    start = (start_room[0] + start_room[2]//2, start_room[1] + start_room[3]//2)
    return grid, rooms, start

grid, rooms, start_pos = generate_dungeon(MAP_W, MAP_H, room_attempts=18)

# place enemies and items
ENEMY_TYPES = {
    "Crawler": {"hp": 10, "atk": 2, "color": "#ff5555"},
    "Stalker": {"hp": 18, "atk": 4, "color": "#ff2222"},
}
entities = []  # each: dict with x,y,type,hp,state,path,target_time
items = {}  # (x,y) -> list of items

for r in rooms:
    # random items and enemies in rooms
    for _ in range(random.randint(0, 2)):
        ix = random.randint(r[0], r[0] + r[2] - 1)
        iy = random.randint(r[1], r[1] + r[3] - 1)
        items.setdefault((ix, iy), []).append(random.choice(["medkit", "knife", "pistol", "ammo"]))
    if random.random() < 0.6:
        ex = random.randint(r[0], r[0] + r[2] - 1)
        ey = random.randint(r[1], r[1] + r[3] - 1)
        entities.append({"x": ex, "y": ey, "type": random.choice(list(ENEMY_TYPES.keys())), "hp": 0, "state": "idle", "path": [], "next_move": 0.0})
for e in entities:
    e["hp"] = ENEMY_TYPES[e["type"]]["hp"]

# player state + inventory
player = {
    "x": start_pos[0],
    "y": start_pos[1],
    "hp": 30,
    "atk": 5,
    "inv": {"medkit": 0},
    "weapon": "knife",  # knife or pistol
    "ammo": 0,
    "facing": (0, 1),
    "anim_frame": 0.0
}

# fog of war: discovered set
discovered = set()
def reveal_area(px, py, r=VIEW_RADIUS):
    for dy in range(-r, r+1):
        for dx in range(-r, r+1):
            tx, ty = px+dx, py+dy
            if 0 <= tx < MAP_W and 0 <= ty < MAP_H and grid[ty][tx] == 0:
                discovered.add((tx, ty))

reveal_area(player["x"], player["y"], VIEW_RADIUS)

# pathfinding A* on grid
def neighbors(node):
    x,y = node
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx,ny = x+dx,y+dy
        if 0<=nx<MAP_W and 0<=ny<MAP_H and grid[ny][nx]==0:
            yield (nx,ny)

def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(start, goal):
    if start == goal: return []
    frontier = [(0, start)]
    came = {start: None}
    cost = {start:0}
    while frontier:
        _, cur = heapq.heappop(frontier)
        if cur==goal:
            # reconstruct
            path=[]
            while cur!=start:
                path.append(cur)
                cur = came[cur]
            path.reverse()
            return path
        for n in neighbors(cur):
            nc = cost[cur] + 1
            if n not in cost or nc < cost[n]:
                cost[n]=nc
                pri = nc + heuristic(n,goal)
                heapq.heappush(frontier, (pri, n))
                came[n]=cur
    return []

# utilities
def passable(x,y):
    return 0<=x<MAP_W and 0<=y<MAP_H and grid[y][x]==0 and not any(e["x"]==x and e["y"]==y for e in entities)

def entity_at(x,y):
    for e in entities:
        if e["x"]==x and e["y"]==y:
            return e
    return None

# particles (list of dict: x,y,vx,vy,life,color,size)
particles = []
def spawn_particles(x,y,count=8,color="#ffcc00",speed=1.6,size=3,life=0.5):
    for _ in range(count):
        a = random.random()*math.tau
        particles.append({"x":x,"y":y,"vx":math.cos(a)*speed,"vy":math.sin(a)*speed,"life":life,"color":color,"size":size})

# drawing helpers
CAM_X = player["x"] * TILE
CAM_Y = player["y"] * TILE
CAM_SMOOTH = 0.25

def world_to_screen(tx,ty):
    sx = tx * TILE - CAM_X
    sy = ty * TILE - CAM_Y
    return sx, sy

def draw_world():
    pen.clear()
    # draw floor and walls only within view box
    left = int((CAM_X - 600) // TILE) - 1
    right = int((CAM_X + 600) // TILE) + 1
    top = int((CAM_Y + 500) // TILE) + 1
    bottom = int((CAM_Y - 500) // TILE) - 1
    for y in range(max(0, bottom), min(MAP_H, top+1)):
        for x in range(max(0, left), min(MAP_W, right+1)):
            sx, sy = world_to_screen(x, y)
            if (x,y) in discovered:
                if grid[y][x] == 0:
                    pen.goto(sx, sy - TILE//2)
                    pen.dot(TILE-2, "#222222")
                else:
                    pen.goto(sx, sy - TILE//2)
                    pen.dot(TILE-6, "#444444")
            else:
                # undiscovered dark tile
                pen.goto(sx, sy - TILE//2)
                pen.dot(TILE-8, "#000000")
    # draw items
    for (ix,iy), ilist in items.items():
        if (ix,iy) in discovered and ilist:
            sx,sy = world_to_screen(ix,iy)
            pen.goto(sx,sy - TILE//4)
            pen.dot(TILE//3, "#ffe066")
    # draw enemies
    for e in entities:
        if (e["x"], e["y"]) in discovered:
            sx,sy = world_to_screen(e["x"], e["y"])
            pen.goto(sx, sy + TILE//4)
            pen.dot(TILE//2, ENEMY_TYPES.get(e["type"], ENEMY_TYPES.setdefault(e["type"], {"color":"#ff4444"}))["color"] if False else ENEMY_TYPES[e["type"]]["color"])
    # fog overlay radial darkness
    overlay_fog()

def overlay_fog():
    # draw a radial gradient-like fog using multiple dots (cheap)
    px,py = player["x"], player["y"]
    for dy in range(-VIEW_RADIUS-1, VIEW_RADIUS+2):
        for dx in range(-VIEW_RADIUS-1, VIEW_RADIUS+2):
            tx,ty = px+dx, py+dy
            if 0<=tx<MAP_W and 0<=ty<MAP_H:
                d = math.hypot(dx, dy)
                sx, sy = world_to_screen(tx, ty)
                if d <= VIEW_RADIUS and (tx,ty) in discovered:
                    # slightly lighter
                    pass
                else:
                    pen.goto(sx, sy - TILE//2)
                    pen.dot(TILE-6, "#000000")

# draw player animated (simple 2-frame bob / muzzle flash)
def draw_player(t):
    player_draw.clear()
    sx, sy = world_to_screen(player["x"], player["y"])
    # base body
    player_draw.goto(sx, sy - 8)
    c = "#ffffff"
    player_draw.dot(TILE//2 + 2, c)
    # weapon indicator
    if player["weapon"] == "pistol" and t > 0:
        # small muzzle flash when fired, but t used by main loop for anim
        player_draw.goto(sx + (player["facing"][0]*8), sy + (player["facing"][1]*8))
        player_draw.dot(8, "#ffcc33")
    # facing mark
    fx, fy = player["facing"]
    player_draw.goto(sx + fx*8, sy + fy*8)
    player_draw.dot(6, "#00ff00")

def draw_particles(dt):
    particles_draw.clear()
    for p in particles:
        sx = p["x"] * TILE - CAM_X
        sy = p["y"] * TILE - CAM_Y
        particles_draw.goto(sx, sy)
        particles_draw.dot(p["size"], p["color"])
        # update
        p["x"] += p["vx"] * dt * 6.0
        p["y"] += p["vy"] * dt * 6.0
        p["life"] -= dt
    # remove dead
    while particles and particles[0]["life"] <= 0:
        particles.pop(0)
    # cleanup any negative life ones
    for i in reversed(range(len(particles))):
        if particles[i]["life"] <= 0:
            particles.pop(i)

# minimap
def draw_minimap():
    mini.clear()
    ox = 380
    oy = 320
    # background
    mini.goto(ox - 2, oy + 2)
    mini.color("#111111")
    mini.begin_fill()
    for _ in range(2):
        mini.forward(MAP_W * MM_TILE + 4)
        mini.right(90)
        mini.forward(MAP_H * MM_TILE + 4)
        mini.right(90)
    mini.end_fill()
    for y in range(MAP_H):
        for x in range(MAP_W):
            mx = ox + x * MM_TILE
            my = oy + (MAP_H - y) * MM_TILE
            mini.goto(mx, my)
            if grid[y][x] == 1:
                mini.dot(MM_TILE, "#444444")
            else:
                mini.dot(MM_TILE, "#222222")
    # enemies
    for e in entities:
        mini.goto(ox + e["x"] * MM_TILE, oy + (MAP_H - e["y"]) * MM_TILE)
        mini.dot(MM_TILE - 1, "#ff4444")
    # player
    mini.goto(ox + player["x"] * MM_TILE, oy + (MAP_H - player["y"]) * MM_TILE)
    mini.dot(MM_TILE - 1, "#00ff00")

# HUD & Inventory
show_inventory = False
def draw_hud():
    hud.clear()
    hud.goto(-560, 380)
    hud.color("#ffffff")
    hud.write(f"HP: {player['hp']}", font=("Courier", 18, "bold"))
    # health bar
    hud.goto(-560, 350)
    hud.color("#333333")
    hud.begin_fill()
    for _ in range(2):
        hud.forward(260)
        hud.right(90)
        hud.forward(20)
        hud.right(90)
    hud.end_fill()
    hud.goto(-560, 350)
    filled = int(260 * max(0, min(1, player["hp"]/30)))
    hud.color("#ff2222")
    hud.begin_fill()
    for _ in range(2):
        hud.forward(filled)
        hud.right(90)
        hud.forward(20)
        hud.right(90)
    hud.end_fill()
    hud.goto(-560, 320)
    hud.color("#dddddd")
    inv_text = ", ".join([f"{k}x{v}" for k,v in player["inv"].items() if v>0]) if player["inv"] else "(empty)"
    hud.write(f"Inv: {inv_text}   Weapon: {player['weapon']} Ammo: {player['ammo']}", font=("Courier", 12, "normal"))
    hud.goto(-560, -380)
    hud.color("#cccccc")
    hud.write("WASD/Arrows move  E pickup  Q use medkit  F melee  R shoot  I inventory  Esc quit", font=("Courier", 10, "normal"))
    if show_inventory:
        draw_inventory_panel()

def draw_inventory_panel():
    hud.goto(-220, 50)
    hud.color("#111111")
    hud.begin_fill()
    for _ in range(2):
        hud.forward(440); hud.right(90); hud.forward(240); hud.right(90)
    hud.end_fill()
    hud.goto(-200, 240)
    hud.color("#ffffff")
    hud.write("Inventory", font=("Courier", 20, "bold"))
    y = 200
    hud.color("#dddddd")
    for k in sorted(player["inv"].keys()):
        hud.goto(-200, y)
        hud.write(f"{k}: {player['inv'][k]}", font=("Courier", 16, "normal"))
        y -= 28
    hud.goto(-200, -10)
    hud.write("Press Q to use medkit. Press R to equip/use pistol (if present).", font=("Courier", 12, "normal"))

# enemy AI tick - roaming + pathfind to player if close
def enemy_ai_tick(dt):
    for e in entities:
        e["next_move"] -= dt
        # if close to player, pathfind
        dist = abs(e["x"] - player["x"]) + abs(e["y"] - player["y"])
        if dist <= 8:
            if e["next_move"] <= 0:
                path = astar((e["x"], e["y"]), (player["x"], player["y"]))
                if path and len(path) > 0:
                    nx, ny = path[0]
                    # if moving into player, attack
                    if nx == player["x"] and ny == player["y"]:
                        player["hp"] -= ENEMY_TYPES.get(e["type"], ENEMY_TYPES.setdefault(e["type"], {"atk":e.get("atk",2)}))["atk"]
                        spawn_particles(player["x"], player["y"], count=10, color="#ff4444", speed=1.0, size=3)
                    else:
                        # move if not blocked by other entities
                        if not entity_at(nx, ny) and grid[ny][nx] == 0:
                            e["x"], e["y"] = nx, ny
                    e["next_move"] = 0.6 + random.random() * 0.6
        else:
            # random roam occasionally
            if e["next_move"] <= 0:
                dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1),(0,0)])
                nx, ny = e["x"] + dx, e["y"] + dy
                if 0 <= nx < MAP_W and 0 <= ny < MAP_H and grid[ny][nx] == 0 and not entity_at(nx, ny):
                    e["x"], e["y"] = nx, ny
                e["next_move"] = 1.0 + random.random() * 2.0

# actions
message = ""
last_shot = 0.0
def pickup():
    global message
    pos = (player["x"], player["y"])
    contents = items.get(pos)
    if not contents:
        message = "Nothing here."
        return
    it = contents.pop(0)
    player["inv"][it] = player["inv"].get(it, 0) + 1
    if it == "pistol":
        # add ammo and equip pistol
        player["ammo"] += 6
        player["weapon"] = "pistol"
    if it == "ammo":
        player["ammo"] += random.randint(2,5)
    message = f"Picked up {it}."
    spawn_particles(player["x"], player["y"], count=10, color="#ffe066", speed=1.6, size=4)

def use_medkit():
    if player["inv"].get("medkit",0) > 0:
        player["inv"]["medkit"] -= 1
        player["hp"] = min(30, player["hp"] + 20)
        spawn_particles(player["x"], player["y"], count=12, color="#88ff88", speed=1.2, size=3)
    else:
        global message
        message = "No medkit."

def melee_attack():
    # hit in facing tile
    fx, fy = player["facing"]
    tx, ty = player["x"] + fx, player["y"] + fy
    e = entity_at(tx, ty)
    if e:
        dmg = player["atk"]
        e["hp"] -= dmg
        spawn_particles(tx, ty, count=10, color="#ff8888", speed=1.8, size=3)
        if e["hp"] <= 0:
            entities.remove(e)
            spawn_particles(tx, ty, count=18, color="#ffcc99", speed=2.2, size=4)
    else:
        # swing particle
        spawn_particles(player["x"] + fx*0.5, player["y"] + fy*0.5, count=6, color="#ffffff", speed=1.0, size=2)

def shoot():
    global last_shot, message
    now = time.perf_counter()
    if now - last_shot < 0.25:
        return
    if player["ammo"] <= 0:
        message = "No ammo."
        return
    last_shot = now
    player["ammo"] -= 1
    # trace ray until wall or hit
    fx, fy = player["facing"]
    bx, by = player["x"], player["y"]
    for step in range(1, 10):
        tx, ty = player["x"] + fx*step, player["y"] + fy*step
        if not (0 <= int(tx) < MAP_W and 0 <= int(ty) < MAP_H):
            break
        if grid[int(ty)][int(tx)] == 1:
            # hit wall, spawn particles
            spawn_particles(tx, ty, count=8, color="#ffaa33", speed=2.0, size=3)
            break
        e = entity_at(int(tx), int(ty))
        if e:
            e["hp"] -= 8 + random.randint(0,4)
            spawn_particles(tx, ty, count=14, color="#ffcc44", speed=2.4, size=4)
            if e["hp"] <= 0:
                entities.remove(e)
                spawn_particles(int(tx), int(ty), count=18, color="#ff9999", speed=2.4, size=4)
            break
        # tracer particles along path
        spawn_particles(tx, ty, count=1, color="#ffeeaa", speed=0.2, size=2, life=0.08)

# key bindings
def try_move(dx,dy):
    nx = player["x"] + dx
    ny = player["y"] + dy
    if 0<=nx<MAP_W and 0<=ny<MAP_H and grid[ny][nx] == 0 and not any(e["x"]==nx and e["y"]==ny for e in entities):
        player["x"], player["y"] = nx, ny
    player["facing"] = (dx, dy) if dx!=0 or dy!=0 else player["facing"]
    reveal_area(player["x"], player["y"], VIEW_RADIUS)

def on_w(): try_move(0,1)
def on_s(): try_move(0,-1)
def on_a(): try_move(-1,0)
def on_d(): try_move(1,0)
def on_up(): try_move(0,1)
def on_down(): try_move(0,-1)
def on_left(): try_move(-1,0)
def on_right(): try_move(1,0)
def on_e(): pickup()
def on_q(): use_medkit()
def on_f(): melee_attack()
def on_r(): shoot()
def on_i():
    global show_inventory
    show_inventory = not show_inventory

wn.listen()
wn.onkey(on_w, "w"); wn.onkey(on_s, "s"); wn.onkey(on_a, "a"); wn.onkey(on_d, "d")
wn.onkey(on_up, "Up"); wn.onkey(on_down, "Down"); wn.onkey(on_left, "Left"); wn.onkey(on_right, "Right")
wn.onkey(on_e, "e"); wn.onkey(on_q, "q"); wn.onkey(on_f, "f"); wn.onkey(on_r, "r"); wn.onkey(on_i, "i")
wn.onkey(lambda: (turtle.bye(), sys.exit()), "Escape")

# ensure player has inventory dict keys
player["inv"].setdefault("medkit", 0)
player["inv"].setdefault("knife", 0)
player["inv"].setdefault("pistol", 0)
player["inv"].setdefault("ammo", 0)

# initial reveal items near start
reveal_area(player["x"], player["y"], VIEW_RADIUS)

# main loop
last_time = time.perf_counter()
acc = 0.0
try:
    while True:
        now = time.perf_counter()
        dt = now - last_time
        last_time = now
        acc += dt
        # tick enemy AI and particles at fixed small steps if dt large
        enemy_ai_tick(dt)
        # update camera
        target_cam_x = player["x"] * TILE
        target_cam_y = player["y"] * TILE
        CAM_X += (target_cam_x - CAM_X) * CAM_SMOOTH if 'CAM_X' in globals() else 0
        CAM_Y += (target_cam_y - CAM_Y) * CAM_SMOOTH if 'CAM_Y' in globals() else 0
        # render
        draw_world()
        # update particles (scale dt)
        draw_particles(dt)
        # draw player
        player["anim_frame"] += dt * 8.0
        draw_player(player["anim_frame"])
        # draw HUD and minimap
        draw_hud()
        draw_minimap()
        # draw particles overlay (already updated)
        wn.update()
        # cap framerate
        sleep_time = FRAME_TIME - (time.perf_counter() - now)
        if sleep_time > 0:
            time.sleep(sleep_time)
except turtle.Terminator:
    pass
