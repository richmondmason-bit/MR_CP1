
#!/usr/bin/env python3
"""
mini_minecraft_pygame.py
A simple 2D side-view block world with placement/removal using Pygame.

Run:
    pip install pygame
    python mini_minecraft_pygame.py
"""
import pygame
import math
import sys

# -------------------------
# Config
# -------------------------
SCREEN_W, SCREEN_H = 1000, 700
TILE = 24                    # tile size in pixels
WORLD_WIDTH = 300            # width in tiles (x)
WORLD_HEIGHT = 80            # height in tiles (y)
GROUND_LEVEL = 12            # base ground height
MAX_HEIGHT = WORLD_HEIGHT - 1
FPS = 60

# Block IDs
AIR = 0
GRASS = 1
DIRT = 2
STONE = 3
WOOD = 4
LEAVES = 5

BLOCKS = {
    0: None,
    1: 'grass',
    2: 'dirt',
    3: 'stone',
    4: 'wood',
    5: 'leaves'
}

# Colors (RGB)
BLOCK_COLORS = {
    1: (106, 170, 88),  # grass
    2: (150, 111, 51),  # dirt
    3: (120, 120, 120), # stone
    4: (160, 110, 60),  # wood
    5: (60, 150, 60),   # leaves
}

BG_COLOR = (135, 206, 235)  # sky blue

# -------------------------
# Simple deterministic noise (same idea as your ursina code)
# -------------------------
def noise(x, z=0.0):
    # returns value roughly between -1 and 1
    return (math.sin(x * 0.7 + z * 0.3) + math.cos(z * 0.4 - x * 0.2)) * 0.5

def terrain_height_at(x):
    """Deterministic height map for given x tile (integer). Returns integer y (0-based from bottom)."""
    # scale x to produce gentle hills
    h = int(GROUND_LEVEL + (noise(x * 0.12, x * 0.08) * 6))
    h = max(1, min(MAX_HEIGHT - 1, h))
    return h

# -------------------------
# World (tile map)
# -------------------------
# store blocks as dict keyed by (x,y)
world = {}

def set_block(wx, wy, block_id):
    if wy < 0 or wy > MAX_HEIGHT or wx < 0 or wx >= WORLD_WIDTH:
        return
    if block_id in (0, None):
        world.pop((wx, wy), None)
    else:
        world[(wx, wy)] = block_id

def get_block(wx, wy):
    return world.get((wx, wy), AIR)

def generate_world():
    for x in range(WORLD_WIDTH):
        h = terrain_height_at(x)
        for y in range(h):
            if y == h - 1:
                set_block(x, y, GRASS)
            elif y >= h - 4:
                set_block(x, y, DIRT)
            else:
                set_block(x, y, STONE)
    # add a few trees
    for x in range(10, WORLD_WIDTH - 10, 16):
        trunk_top = terrain_height_at(x)
        # trunk
        set_block(x, trunk_top, WOOD)
        set_block(x, trunk_top + 1, WOOD)
        # leaves
        for lx in (-1,0,1):
            for ly in (2,3,4):
                set_block(x + lx, trunk_top + ly, LEAVES)

# -------------------------
# Player
# -------------------------
class Player:
    def __init__(self, x, y):
        self.x = x  # float tile coordinates
        self.y = y
        self.w = 0.8   # in tiles
        self.h = 1.8   # in tiles
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 7.0    # tiles/sec
        self.jump_speed = 12.0
        self.on_ground = False

    def rect(self):
        # returns pixel rect around player for drawing, but collision uses tile coordinates
        return pygame.Rect(0,0, int(self.w * TILE), int(self.h * TILE))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update(self, dt, keys):
        # horizontal input
        ax = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            ax = -1.0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            ax = 1.0
        self.vx = ax * self.speed

        # gravity
        self.vy -= 30.0 * dt  # strong gravity
        if self.vy < -60:
            self.vy = -60

        # jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vy = self.jump_speed
            self.on_ground = False

        # apply motion and do collisions (tile-based)
        self._apply_motion(dt)

    def _apply_motion(self, dt):
        # horizontal first
        new_x = self.x + self.vx * dt
        if not self._collides_at(new_x, self.y):
            self.x = new_x
        else:
            # try small steps to avoid tunneling
            sign = 1 if self.vx > 0 else -1
            step = 0.05 * sign
            while abs(self.vx) > 0.001:
                new_x = self.x + step
                if self._collides_at(new_x, self.y):
                    break
                self.x = new_x
                break
            self.vx = 0

        # vertical
        new_y = self.y + self.vy * dt
        if not self._collides_at(self.x, new_y):
            self.y = new_y
            self.on_ground = False
        else:
            # collided: if moving down, stand on block; if moving up, hit ceiling
            if self.vy < 0:
                # place on top of block
                self.on_ground = True
                # align to top of the tile we stand on
                # find the highest integer y such that no collision at that y
                yt = math.floor(self.y)
                # step down until free?
                # we'll snap to nearest non-colliding position with small steps upward
                # attempt to find y where collides_at(x, y - eps) is False
                # simpler: increment y from integer down to make player rest
                self.y = math.ceil(new_y)  # conservative
            else:
                # hit ceiling -> stop upward movement
                pass
            self.vy = 0

    def _collides_at(self, x, y):
        # Check tile by tile overlapping player's bounding box
        left = math.floor(x - 0.0001)
        right = math.floor(x + self.w - 0.0001)
        bottom = math.floor(y - 0.0001)
        top = math.floor(y + self.h - 0.0001)
        for tx in range(left, right+1):
            for ty in range(bottom, top+1):
                if tx < 0 or tx >= WORLD_WIDTH or ty < 0:
                    # out-of-bounds below ground is collision
                    if ty < 0:
                        return True
                    continue
                if get_block(tx, ty) != AIR:
                    return True
        return False

# -------------------------
# Pygame UI & main loop
# -------------------------
def world_to_screen(wx, wy, camera_x, camera_y):
    """tile coords to pixel coords"""
    sx = (wx - camera_x) * TILE + SCREEN_W // 2
    sy = SCREEN_H - ((wy - camera_y) * TILE + SCREEN_H // 4)  # shift camera vertically a bit
    return int(sx), int(sy)

def screen_to_world(px, py, camera_x, camera_y):
    wx = (px - SCREEN_W // 2) / TILE + camera_x
    wy = ((SCREEN_H - py) - SCREEN_H // 4) / TILE + camera_y
    return int(round(wx)), int(round(wy))

def draw_world(surface, camera_x, camera_y):
    # draw sky/background
    surface.fill(BG_COLOR)

    # compute visible tile range for efficiency
    half_w_tiles = SCREEN_W // TILE // 2 + 3
    half_h_tiles = SCREEN_H // TILE // 2 + 3
    start_x = max(0, int(math.floor(camera_x)) - half_w_tiles)
    end_x = min(WORLD_WIDTH - 1, int(math.floor(camera_x)) + half_w_tiles)
    start_y = 0
    end_y = min(WORLD_HEIGHT - 1, int(math.floor(camera_y)) + half_h_tiles)

    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            b = get_block(x, y)
            if b == AIR:
                continue
            sx, sy = world_to_screen(x, y, camera_x, camera_y)
            rect = pygame.Rect(sx, sy - TILE, TILE, TILE)  # note sy is top-left of the top-left corner of tile's top
            pygame.draw.rect(surface, BLOCK_COLORS.get(b, (255,255,255)), rect)
            # tile border
            pygame.draw.rect(surface, (0,0,0), rect, 1)

def draw_player(surface, player, camera_x, camera_y):
    sx, sy = world_to_screen(player.x, player.y + player.h, camera_x, camera_y)  # convert top-left
    w = int(player.w * TILE)
    h = int(player.h * TILE)
    rect = pygame.Rect(sx, sy, w, h)
    pygame.draw.rect(surface, (200, 40, 40), rect)
    pygame.draw.rect(surface, (0,0,0), rect, 2)

def draw_ui(surface, selected_block):
    font = pygame.font.SysFont("arial", 18)
    lines = [
        "LMB: remove  |  RMB: place  |  1-5: select block  |  WASD/Arrows: move  |  Space: jump",
        f"Selected: {BLOCKS.get(selected_block,'none')} ({selected_block})"
    ]
    y = 8
    for line in lines:
        txt = font.render(line, True, (0,0,0))
        bg = pygame.Surface((txt.get_width()+8, txt.get_height()+4))
        bg.set_alpha(200)
        bg.fill((255,255,255))
        surface.blit(bg, (8, y))
        surface.blit(txt, (12, y+2))
        y += txt.get_height() + 6

    # draw small block palette
    for i in range(1,6):
        bx = 8 + (i-1) * (TILE + 6)
        by = SCREEN_H - (TILE + 12)
        rect = pygame.Rect(bx, by, TILE, TILE)
        if i == selected_block:
            pygame.draw.rect(surface, (255, 215, 0), rect.inflate(6,6))  # highlight
        if i in BLOCK_COLORS:
            pygame.draw.rect(surface, BLOCK_COLORS[i], rect)
            pygame.draw.rect(surface, (0,0,0), rect, 2)
        else:
            pygame.draw.rect(surface, (200,200,200), rect)
            pygame.draw.rect(surface, (0,0,0), rect, 2)
        label = pygame.font.SysFont("arial", 14).render(str(i), True, (0,0,0))
        surface.blit(label, (bx + 4, by + 4))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Mini Minecraft (Pygame)")

    generate_world()

    # place player near center
    start_x = WORLD_WIDTH // 2
    start_y = terrain_height_at(start_x) + 3
    player = Player(start_x + 0.5, start_y)

    camera_x = player.x
    camera_y = player.y + 3

    selected_block = GRASS

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    selected_block = event.key - pygame.K_0
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                wx, wy = screen_to_world(mx, my, camera_x, camera_y)
                if event.button == 1:
                    # Left click -> remove
                    set_block(wx, wy, AIR)
                elif event.button == 3:
                    # Right click -> place selected (if empty)
                    if get_block(wx, wy) == AIR:
                        set_block(wx, wy, selected_block)

        keys = pygame.key.get_pressed()
        player.update(dt, keys)

        # camera follow with smoothing
        camera_x += (player.x - camera_x) * min(10*dt, 1)
        camera_y += ((player.y + 2) - camera_y) * min(10*dt, 1)

        # draw
        draw_world(screen, camera_x, camera_y)
        draw_player(screen, player, camera_x, camera_y)
        draw_ui(screen, selected_block)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()


