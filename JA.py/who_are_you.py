#!/usr/bin/env python
"""
Advanced terminal platformer (single-file).
Cleaned version:
- Removed duplicate/broken classes
- Added Level.parse() to populate enemies, powerups, checkpoints
- Fixed Projectile and Particle single definitions
- Fixed InputCollector.snapshot() to avoid stuck keys
- Improved pause/ESC handling and restart
Note: I preserved your tick-scaling style (uses dt / TICK_RATE in movement)
"""

import os
import sys
import time
import random
import threading

# -------------------
# Input (cross-platform)
# -------------------
if os.name == 'nt':
    import msvcrt

    def get_key_nonblocking():
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            try:
                return ch.decode('utf-8').lower()
            except:
                return None
        return None

    def get_key_blocking():
        while True:
            ch = msvcrt.getch()
            try:
                return ch.decode('utf-8').lower()
            except:
                pass

else:
    import tty, termios, select

    def get_key_nonblocking():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            dr, dw, de = select.select([sys.stdin], [], [], 0)
            if dr:
                ch = sys.stdin.read(1)
                return ch.lower()
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def get_key_blocking():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            return ch.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

# -------------------
# Simple clear
# -------------------
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# -------------------
# Game constants
# -------------------
TICK_RATE = 0.06  # seconds per tick (~16 FPS)
VIEWPORT_W = 40
VIEWPORT_H = 16
GRAVITY = 0.5
TERMINAL_V = 3.5
WALK_ACCEL = 0.6
FRICTION = 0.75
JUMP_POWER = -4.5
DASH_SPEED = 5
PROJECTILE_SPEED = 6
INVINCIBLE_TIME = 4.0

# -------------------
# Utility
# -------------------
def clamp(v, a, b):
    return max(a, min(b, v))

# -------------------
# Level representation
# Use a list of strings; Level stores mutable rows internally
# '#' = solid ground/platform
# '-' = platform (single-tile)
# 'H' = ladder
# 'C' = checkpoint
# '*' = powerup
# 'S' = spike (stationary hazard)
# '.' = empty
# 'E' = enemy spawn (converted by parser)
# -------------------
LEVELS = [
    [
        "..............................................................",
        "..............................................................",
        "..............................................................",
        ".....................*........................................",
        "...............###.............H..............................",
        "................................H...........E................",
        "......###.......................H............................",
        "................................H...............###..........",
        "....E..............###............................*..........",
        "##############################......###......................",
        "..............................................................",
        "...............C............................................#",
        "###########################.............###########..........",
        "..............................................................",
        "..............................................................",
        "..............................................................",
    ],
    [
        "..............................................................",
        "..........E..............................................*....",
        "..............................................................",
        "........####..............###..........................###....",
        "........................................H.....................",
        "....*......................H...........E..............E......",
        "...................###....H.................................",
        ".........................H..............###.................",
        "....C.............................###..................S....",
        "######################....###############################....",
        "..............................................................",
        "...........................................*..................",
        "..................###........................................",
        ".......................................................E......",
        "..............................................................",
        "..............................................................",
    ]
]

# -------------------
# Game classes
# -------------------
class Level:
    def __init__(self, layout):
        # layout: list of strings
        # store as mutable rows of chars for parsing
        self.rows = [list(r) for r in layout]
        self.h = len(self.rows)
        self.w = len(self.rows[0]) if self.h > 0 else 0
        self.enemies_to_spawn = []
        self.powerups = {}  # (x,y) -> type
        self.checkpoints = set()
        self.parse()

    def parse(self):
        """Scan rows and convert markers into runtime structures."""
        for y in range(self.h):
            for x in range(self.w):
                c = self.rows[y][x]
                if c == 'E':
                    self.enemies_to_spawn.append((x, y))
                    self.rows[y][x] = '.'
                elif c == '*':
                    # assign a random powerup type
                    self.powerups[(x, y)] = random.choice(['jump', 'speed', 'health', 'invul'])
                    self.rows[y][x] = '.'
                elif c == 'C':
                    self.checkpoints.add((x, y))
                    self.rows[y][x] = '.'

    def tile(self, x, y):
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return '#'  # out-of-bounds treated as solid
        return self.rows[y][x]

    def is_solid(self, x, y):
        t = self.tile(x, y)
        return t == '#'

    def is_platform(self, x, y):
        t = self.tile(x, y)
        return t in ('-', '#')

    def is_ladder(self, x, y):
        return self.tile(x, y) == 'H'

    def is_spike(self, x, y):
        return self.tile(x, y) == 'S'

class Particle:
    def __init__(self, x, y, char='*', life=0.3):
        self.x = x
        self.y = y
        self.char = char
        self.life = life

    def update(self, dt):
        self.life -= dt

class Projectile:
    def __init__(self, x, y, vx, owner):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.owner = owner  # 'player' or 'enemy'
        self.char = '-'

    def update(self, dt):
        # keep your original tick scaling behavior: scale movement by dt / TICK_RATE
        self.x += self.vx * (dt / TICK_RATE) * PROJECTILE_SPEED

class Enemy:
    def __init__(self, x, y, typ='patroller'):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.typ = typ
        self.dir = random.choice([-1, 1])
        self.alive = True
        self.char = 'E' if typ != 'spike' else 'S'
        self.on_ground = False
        self.patrol_range = 6
        self.patrol_center = x

    def bbox(self):
        return int(round(self.x)), int(round(self.y))

    def update(self, level, dt):
        if not self.alive:
            return
        if self.typ == 'spike':
            return  # stationary hazard
        if self.typ == 'patroller':
            speed = 0.8
            target = self.patrol_center + self.dir * self.patrol_range
            if abs(self.x - target) < 0.2:
                self.dir *= -1
            self.vx = self.dir * speed
        elif self.typ == 'jumper':
            if self.on_ground and random.random() < 0.04:
                self.vy = -3.2
            self.vx = self.dir * 0.5
        elif self.typ == 'flyer':
            self.vy = 0.8 * (0.5 - random.random())
            self.vx = self.dir * 0.6

        # apply physics (use your original tick scaling)
        self.vy += GRAVITY * (dt / TICK_RATE)
        self.vy = clamp(self.vy, -TERMINAL_V, TERMINAL_V)

        newx = self.x + self.vx * (dt / TICK_RATE)
        newy = self.y + self.vy * (dt / TICK_RATE)

        # simple collision with level solid tiles (single tile body)
        if level.is_solid(int(round(newx)), int(round(self.y))):
            self.vx = -self.vx
            newx = self.x
            self.dir *= -1
        if level.is_solid(int(round(newx)), int(round(newy))):
            # vertical block
            if self.vy > 0:
                # landed
                self.on_ground = True
                self.vy = 0
                newy = int(round(newy)) - 1
            else:
                self.vy = 0
        else:
            self.on_ground = False

        self.x = newx
        self.y = newy

class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.on_ladder = False
        self.facing = 1
        self.score = 0
        self.lives = 3
        self.checkpoint = (x, y)
        self.invincible_timer = 0.0
        self.speed_mult = 1.0
        self.jump_mult = 1.0
        self.projectiles_remaining = 20
        self.dash_cooldown = 0.0
        self.char = 'P'

    def bbox(self):
        return int(round(self.x)), int(round(self.y))

    def respawn(self):
        self.x, self.y = float(self.checkpoint[0]), float(self.checkpoint[1])
        self.vx = self.vy = 0.0
        self.invincible_timer = 2.0

    def apply_power(self, ptype):
        if ptype == 'jump':
            self.jump_mult = 1.6
            self.score += 50
        elif ptype == 'speed':
            self.speed_mult = 1.6
            self.score += 50
        elif ptype == 'health':
            self.lives += 1
            self.score += 100
        elif ptype == 'invul':
            self.invincible_timer = max(self.invincible_timer, INVINCIBLE_TIME)
            self.score += 75

    def update(self, level, input_state, dt):
        # dt: seconds since last frame. Many physics operations below use dt/TICK_RATE
        target = 0
        if 'a' in input_state:
            target -= 1
            self.facing = -1
        if 'd' in input_state:
            target += 1
            self.facing = 1

        # Ladder behavior
        if level.is_ladder(int(round(self.x)), int(round(self.y))):
            self.on_ladder = True
        else:
            self.on_ladder = False

        if self.on_ladder:
            # ladder vertical control (move per tick scaling to maintain feel)
            if 'w' in input_state:
                self.y -= 1 * (dt / TICK_RATE)
            elif 's' in input_state:
                self.y += 1 * (dt / TICK_RATE)
            # no gravity while on ladder
            self.vy = 0
        else:
            # apply horizontal acceleration
            if target != 0:
                self.vx += target * WALK_ACCEL * self.speed_mult
            else:
                # friction
                self.vx *= FRICTION
            # clamp horizontal speed
            self.vx = clamp(self.vx, -4 * self.speed_mult, 4 * self.speed_mult)

            # gravity
            self.vy += GRAVITY * (dt / TICK_RATE)
            self.vy = clamp(self.vy, -TERMINAL_V * 2, TERMINAL_V)

            # jump
            if 'w' in input_state and self.on_ground:
                self.vy = JUMP_POWER * self.jump_mult
                self.on_ground = False

        # dash / melee on 'q' (cooldown)
        dash = False
        if 'q' in input_state and self.dash_cooldown <= 0:
            dash = True
            self.dash_cooldown = 0.9

        # apply movement and collision
        newx = self.x + self.vx * (dt / TICK_RATE)
        newy = self.y + self.vy * (dt / TICK_RATE)

        # horizontal collision
        if level.is_solid(int(round(newx)), int(round(self.y))):
            # bump and stop
            self.vx = 0
            newx = self.x

        # vertical collision
        if level.is_solid(int(round(newx)), int(round(newy))):
            # landed or hit head
            if self.vy > 0:
                self.on_ground = True
            self.vy = 0
            # set newy to stand on top
            newy = int(round(newy)) - 1
        else:
            self.on_ground = False

        self.x = newx
        self.y = newy

        # timers (these are in real seconds)
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            if self.invincible_timer < 0: self.invincible_timer = 0
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt
            if self.dash_cooldown < 0: self.dash_cooldown = 0

        return dash

# -------------------
# Game manager
# -------------------
class Game:
    def __init__(self, raw_levels):
        # raw_levels: list of list-of-strings (LEVELS)
        self.levels = [Level(l) for l in raw_levels]
        self.level_index = 0
        self.level = self.levels[self.level_index]
        sp = self.find_spawn(self.level)
        self.player = Player(sp[0], sp[1])
        self.populate_enemies()
        self.projectiles = []
        self.enemy_projectiles = []
        self.particles = []
        self.running = True
        self.paused = False
        self.last_tick = time.time()
        self.view_x = 0
        self.view_y = 0
        self.tick_count = 0
        self.elapsed = 0.0
        self.start_time = time.time()
        self.game_over = False

    def find_spawn(self, level):
        for y in range(level.h - 1):
            for x in range(level.w):
                # if tile is empty and tile below is solid/platform -> spawn here
                if not level.is_solid(x, y) and level.is_platform(x, y + 1):
                    return (x, y)
        return (1, 1)

    def populate_enemies(self):
        self.enemies = []
        for sx, sy in self.level.enemies_to_spawn:
            typ = random.choice(['patroller', 'jumper', 'flyer'])
            if random.random() < 0.08:
                typ = 'spike'
            e = Enemy(float(sx), float(sy), typ=typ)
            e.patrol_center = sx
            self.enemies.append(e)

    def spawn_particle(self, x, y, char='*', life=0.35):
        self.particles.append(Particle(x, y, char, life))

    def spawn_projectile(self, x, y, dir, owner='player'):
        vx = dir
        p = Projectile(x, y, vx, owner)
        if owner == 'player':
            self.projectiles.append(p)
        else:
            self.enemy_projectiles.append(p)

    def update(self, dt, input_state):
        if self.game_over or self.paused:
            return

        self.tick_count += 1
        self.elapsed = time.time() - self.start_time

        # player update (passes real dt; player uses dt/TICK_RATE internally for physics)
        did_dash = self.player.update(self.level, input_state, dt)

        # if dashed: damage nearby enemies
        if did_dash:
            self.player.vx = DASH_SPEED * self.player.facing
            px, py = self.player.bbox()
            hit_any = False
            for e in self.enemies:
                ex, ey = e.bbox()
                if abs(ex - px - self.player.facing) <= 1 and abs(ey - py) <= 1:
                    e.alive = False
                    self.player.score += 200
                    hit_any = True
                    self.spawn_particle(ex, ey, 'x', 0.5)
            if hit_any:
                self.spawn_particle(px + self.player.facing, py, '/', 0.3)

        # shooting: 'f' to shoot (if available)
        if 'f' in input_state and self.player.projectiles_remaining > 0:
            px, py = self.player.bbox()
            self.spawn_projectile(px + self.player.facing, py, self.player.facing, owner='player')
            self.player.projectiles_remaining -= 1

        # update projectiles (player)
        for p in list(self.projectiles):
            p.update(dt)
            tx, ty = int(round(p.x)), int(round(p.y))
            if self.level.is_solid(tx, ty) or tx < 0 or tx >= self.level.w:
                try:
                    self.projectiles.remove(p)
                except ValueError:
                    pass
                self.spawn_particle(tx, ty, '-', 0.25)
                continue
            for e in self.enemies:
                ex, ey = e.bbox()
                if e.alive and int(round(p.x)) == ex and int(round(p.y)) == ey:
                    e.alive = False
                    if p in self.projectiles:
                        try:
                            self.projectiles.remove(p)
                        except ValueError:
                            pass
                    self.player.score += 150
                    self.spawn_particle(ex, ey, 'x', 0.35)
                    break

        # enemy projectiles
        for p in list(self.enemy_projectiles):
            p.update(dt)
            tx, ty = int(round(p.x)), int(round(p.y))
            if self.level.is_solid(tx, ty) or tx < 0 or tx >= self.level.w:
                try:
                    self.enemy_projectiles.remove(p)
                except ValueError:
                    pass
                continue
            px, py = self.player.bbox()
            if int(round(p.x)) == px and int(round(p.y)) == py:
                if self.player.invincible_timer <= 0:
                    self.player.lives -= 1
                    self.player.invincible_timer = 2.0
                    self.player.respawn()
                if p in self.enemy_projectiles:
                    try:
                        self.enemy_projectiles.remove(p)
                    except ValueError:
                        pass

        # update enemies
        for e in list(self.enemies):
            if not e.alive:
                continue
            e.update(self.level, dt)
            ex, ey = e.bbox()
            px, py = self.player.bbox()
            # collision with player
            if ex == px and ey == py:
                if self.player.invincible_timer <= 0:
                    self.player.lives -= 1
                    self.player.invincible_timer = 2.0
                    self.player.respawn()
            # spike check via level tile underneath
            if self.level.is_spike(int(round(e.x)), int(round(e.y))):
                e.alive = False

        # collect powerups
        px, py = self.player.bbox()
        ppos = (px, py)
        if ppos in self.level.powerups:
            ptype = self.level.powerups.pop(ppos)
            self.player.apply_power(ptype)
            self.spawn_particle(px, py, '+', 0.4)

        # checkpoint
        if (px, py) in self.level.checkpoints:
            self.player.checkpoint = (px, py)
            self.player.score += 20
            self.spawn_particle(px, py, 'C', 0.5)

        # if fell off bottom
        if py >= self.level.h - 1 or py < 0:
            self.player.lives -= 1
            self.player.respawn()

        # remove dead enemies
        self.enemies = [e for e in self.enemies if e.alive]

        # maybe spawn some enemy projectiles randomly from flying enemies
        for e in self.enemies:
            if e.typ == 'flyer' and random.random() < 0.01:
                self.spawn_projectile(e.x - 1, e.y, -1, owner='enemy')

        # update particles
        for pr in list(self.particles):
            pr.update(dt)
            if pr.life <= 0:
                try:
                    self.particles.remove(pr)
                except ValueError:
                    pass

        # update camera to follow player (scrolling)
        self.view_x = clamp(int(self.player.x) - VIEWPORT_W // 2, 0, max(0, self.level.w - VIEWPORT_W))
        self.view_y = clamp(int(self.player.y) - VIEWPORT_H // 2, 0, max(0, self.level.h - VIEWPORT_H))

        # level end condition: reach rightmost side of level (win)
        if int(round(self.player.x)) >= self.level.w - 1:
            self.level_index += 1
            if self.level_index >= len(self.levels):
                self.game_over = True
            else:
                self.level = self.levels[self.level_index]
                self.player.checkpoint = self.find_spawn(self.level)
                self.player.respawn()
                self.populate_enemies()

        # game over if no lives
        if self.player.lives <= 0:
            self.game_over = True

    def render(self):
        clear()
        if self.game_over:
            print("=== GAME COMPLETE / OVER ===")
            print(f"Score: {self.player.score}")
            print(f"Time: {int(self.elapsed)}s   Ticks: {self.tick_count}")
            print()
            print("Press 'r' to restart or 'q' to quit.")
            return

        # draw viewport
        ox, oy = self.view_x, self.view_y
        out_lines = []
        for vy in range(VIEWPORT_H):
            y = oy + vy
            line = []
            for vx in range(VIEWPORT_W):
                x = ox + vx
                ch = self.level.tile(x, y)
                # draw solid tile
                if ch == '#':
                    char = '#'
                elif ch == 'H':
                    char = 'H'
                elif ch == 'S':
                    char = '^'
                elif ch == '-':
                    char = '_'
                else:
                    char = ' '
                line.append(char)
            out_lines.append(line)

        # draw powerups
        for (px, py), typ in self.level.powerups.items():
            if ox <= px < ox + VIEWPORT_W and oy <= py < oy + VIEWPORT_H:
                out_lines[py - oy][px - ox] = '*'

        # draw checkpoints
        for (cx, cy) in self.level.checkpoints:
            if ox <= cx < ox + VIEWPORT_W and oy <= cy < oy + VIEWPORT_H:
                out_lines[cy - oy][cx - ox] = 'C'

        # draw enemies
        for e in self.enemies:
            ex, ey = e.bbox()
            if ox <= ex < ox + VIEWPORT_W and oy <= ey < oy + VIEWPORT_H:
                out_lines[ey - oy][ex - ox] = e.char

        # draw projectiles
        for p in self.projectiles + self.enemy_projectiles:
            tx, ty = int(round(p.x)), int(round(p.y))
            if ox <= tx < ox + VIEWPORT_W and oy <= ty < oy + VIEWPORT_H:
                out_lines[ty - oy][tx - ox] = p.char

        # draw particles
        for pr in self.particles:
            tx, ty = int(round(pr.x)), int(round(pr.y))
            if ox <= tx < ox + VIEWPORT_W and oy <= ty < oy + VIEWPORT_H:
                out_lines[ty - oy][tx - ox] = pr.char

        # draw player (with blink if invincible)
        px, py = self.player.bbox()
        if ox <= px < ox + VIEWPORT_W and oy <= py < oy + VIEWPORT_H:
            char = self.player.char
            if self.player.invincible_timer > 0 and int(self.player.invincible_timer * 6) % 2 == 0:
                char = 'p'  # blinking
            out_lines[py - oy][px - ox] = char

        # compose and print
        for row in out_lines:
            print(''.join(row))

        # HUD
        print("-" * VIEWPORT_W)
        print(f"Level: {self.level_index + 1}/{len(self.levels)}  Score: {self.player.score}  Lives: {self.player.lives}  Time: {int(self.elapsed)}s")
        print(f"Proj: {self.player.projectiles_remaining}  Inv: {int(self.player.invincible_timer)}s  DashCD: {round(self.player.dash_cooldown,1)}s")
        print("Controls: a/d = move, w = jump/climb, s = down, f = shoot, q = dash/melee, p = pause, r = restart, ESC = quit")

    def restart(self):
        # reinitialize from global LEVELS
        self.__init__(LEVELS)

# -------------------
# Input thread to collect keypresses into a state set
# -------------------
class InputCollector(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.pressed = set()
        self.lock = threading.Lock()
        self.running = True

    def run(self):
        # Non-blocking poll loop
        while self.running:
            k = get_key_nonblocking()
            if k:
                with self.lock:
                    if k in ('a','d','w','s','f','q','p','r'):
                        # add key to set (we will snapshot and clear)
                        self.pressed.add(k)
                    elif ord(k) == 27:  # ESC
                        self.pressed.add('esc')
            time.sleep(0.01)

    def snapshot(self):
        # produce a snapshot copy and clear all collected keys
        with self.lock:
            s = set(self.pressed)
            self.pressed.clear()
            return s

    def stop(self):
        self.running = False

# -------------------
# Main loop & screens
# -------------------
def title_screen():
    clear()
    print("========================================")
    print("         TERMINAL PLATFORMER 2.0        ")
    print("========================================")
    print()
    print("Controls: a/d = move, w = jump/climb, s = down, f = shoot, q = dash/melee")
    print()
    print("Features: multiple levels, ladders, powerups, enemies, checkpoints")
    print()
    print("Press Enter to start, or q to quit.")
    while True:
        k = get_key_blocking()
        if k in ('\r','\n'):
            return True
        if k == 'q' or k == 'Q' or k == '\x1b':
            return False

def pause_screen():
    print("--- PAUSED ---  press p to resume or ESC to quit")
    while True:
        k = get_key_blocking()
        if k == 'p':
            return None
        if ord(k) == 27:
            return 'quit'

def main():
    if not title_screen():
        print("Goodbye.")
        return

    game = Game(LEVELS)
    input_thread = InputCollector()
    input_thread.start()

    last_time = time.time()

    try:
        while True:
            now = time.time()
            dt = now - last_time
            last_time = now

            # snapshot input
            inputs = input_thread.snapshot()

            # handle special keys instantly
            if 'esc' in inputs:
                break
            if 'r' in inputs:
                game.restart()
            if 'p' in inputs:
                game.paused = not game.paused
                if game.paused:
                    game.render()
                    print("(paused) Press 'p' to resume or ESC to quit")
                    res = pause_screen()
                    if res == 'quit':
                        break
                    last_time = time.time()
                continue

            # Build input_state set for player continuous keys
            input_state = set()
            for k in inputs:
                if k in ('a','d','w','s','f','q'):
                    input_state.add(k)

            # update
            game.update(dt, input_state)

            # render
            game.render()

            # if game over, wait for r or q
            if game.game_over:
                k = get_key_blocking()
                if k == 'r':
                    game.restart()
                    last_time = time.time()
                    continue
                elif k == 'q' or k == '\x1b':
                    break

            time.sleep(TICK_RATE)

    except KeyboardInterrupt:
        pass
    finally:
        input_thread.stop()
        clear()
        print("Exiting. Thanks for playing!")

if __name__ == '__main__':
    main()
