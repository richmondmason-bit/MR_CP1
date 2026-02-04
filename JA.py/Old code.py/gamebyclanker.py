import pygame, math, random, time, sys

# ================= CONFIG =================
W, H = 960, 720
FPS = 60

# Colors
COL_BG = (15, 15, 20)
COL_GRID = (25, 25, 35)
COL_P = (0, 255, 200)       # Player
COL_E_GRUNT = (255, 80, 50) # Basic Enemy
COL_E_SNIPER = (255, 220, 0)# Sniper
COL_E_BOMBER = (255, 255, 255) # Exploder
COL_SCRAP = (180, 180, 255) # Currency
COL_TXT = (255, 255, 255)
COL_SHOP = (40, 40, 50)

# ================= VISUALS =================

class Particle:
    def __init__(self, x, y, vx, vy, color, life, size=3, shrink=True):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.shrink = shrink

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    def draw(self, surface):
        if self.life <= 0: return
        alpha = int((self.life / self.max_life) * 255)
        current_size = self.size * (self.life / self.max_life) if self.shrink else self.size
        if current_size < 1: return
        
        s = pygame.Surface((int(current_size)*2, int(current_size)*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (int(current_size), int(current_size)), int(current_size))
        surface.blit(s, (self.x - current_size, self.y - current_size))

class FloatingText:
    def __init__(self, x, y, text, color=(255,255,255)):
        self.x, self.y = x, y
        self.text = str(text)
        self.color = color
        self.life = 0.8
        self.vy = -60

    def update(self, dt):
        self.y += self.vy * dt
        self.life -= dt

# ================= GAME ENGINE =================

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        self.display = pygame.Surface((W, H)) # Draw here first for screenshake
        pygame.display.set_caption("Roguelite V5: Definitive Edition")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_s = pygame.font.SysFont("consolas", 16)
        self.font_m = pygame.font.SysFont("consolas", 24, bold=True)
        self.font_l = pygame.font.SysFont("consolas", 48, bold=True)

        self.reset_game()

    def reset_game(self):
        # Stats
        self.wave = 1
        self.scrap = 0
        self.state = "PLAY" # PLAY, SHOP, GAMEOVER
        self.shake = 0
        
        # Player
        self.p = {
            "x": W//2, "y": H//2, "vx": 0, "vy": 0,
            "hp": 100, "max_hp": 100,
            "spd_mult": 1.0, "dash_cd": 0, "dash_max": 0.8,
            "gun_idx": 0, "reloading": False, "reload_timer": 0
        }
        
        # Weapons
        self.guns = [
            {"name": "Pistol", "dmg": 25, "mag": 12, "cur": 12, "cd": 0.20, "last": 0, "auto": False, "spd": 800, "spread": 2, "pellets": 1},
            {"name": "SMG",    "dmg": 12, "mag": 35, "cur": 35, "cd": 0.08, "last": 0, "auto": True,  "spd": 900, "spread": 8, "pellets": 1},
            {"name": "Shotty", "dmg": 18, "mag": 6,  "cur": 6,  "cd": 0.90, "last": 0, "auto": False, "spd": 750, "spread": 25,"pellets": 6},
        ]

        self.entities = {
            "bullets": [], "e_bullets": [], "enemies": [], "particles": [], "texts": [], "scraps": []
        }
        
        self.start_wave()

    def start_wave(self):
        self.state = "PLAY"
        self.entities["bullets"].clear()
        self.entities["e_bullets"].clear()
        
        # Spawn logic
        count = 5 + int(self.wave * 2.5)
        for _ in range(count):
            self.spawn_enemy()

    def spawn_enemy(self):
        # Random edge spawn
        side = random.choice("tblr")
        if side=="t": x, y = random.randint(0,W), -40
        elif side=="b": x, y = random.randint(0,W), H+40
        elif side=="l": x, y = -40, random.randint(0,H)
        else: x, y = W+40, random.randint(0,H)
        
        # Enemy Types
        roll = random.random()
        etype = "grunt"
        hp, spd, color = 60 + (self.wave*10), 120, COL_E_GRUNT
        
        if self.wave > 2 and roll < 0.2: 
            etype = "sniper"
            hp, spd, color = 40 + (self.wave*5), 90, COL_E_SNIPER
        elif self.wave > 3 and roll > 0.85:
            etype = "bomber"
            hp, spd, color = 30 + (self.wave*5), 190, COL_E_BOMBER

        self.entities["enemies"].append({
            "x": x, "y": y, "vx": 0, "vy": 0,
            "hp": hp, "max_hp": hp, "spd": spd,
            "type": etype, "color": color,
            "atk_cd": 2.0 # For snipers/bombers
        })

    # ================= UPDATE LOOP =================

    def update(self, dt):
        # Screen Shake Decay
        if self.shake > 0: self.shake = max(0, self.shake - 50 * dt)

        # --- PARTICLES & TEXT (Always update) ---
        for p in self.entities["particles"][:]:
            p.update(dt)
            if p.life <= 0: self.entities["particles"].remove(p)
        for t in self.entities["texts"][:]:
            t.update(dt)
            if t.life <= 0: self.entities["texts"].remove(t)

        if self.state == "PLAY":
            self.update_play(dt)
        elif self.state == "SHOP":
            self.update_shop()

    def update_play(self, dt):
        keys = pygame.key.get_pressed()
        p = self.p
        
        # 1. Weapon Switching & Reload
        if keys[pygame.K_1]: p["gun_idx"] = 0; p["reloading"] = False
        if keys[pygame.K_2]: p["gun_idx"] = 1; p["reloading"] = False
        if keys[pygame.K_3]: p["gun_idx"] = 2; p["reloading"] = False
        
        if keys[pygame.K_r] and not p["reloading"]:
             gun = self.guns[p["gun_idx"]]
             if gun["cur"] < gun["mag"]:
                 p["reloading"] = True
                 p["reload_timer"] = 1.0

        if p["reloading"]:
            p["reload_timer"] -= dt
            if p["reload_timer"] <= 0:
                p["reloading"] = False
                self.guns[p["gun_idx"]]["cur"] = self.guns[p["gun_idx"]]["mag"]

        # 2. Movement & Dash
        acc = 1800
        fric = 10
        input_x = (keys[pygame.K_d] - keys[pygame.K_a])
        input_y = (keys[pygame.K_s] - keys[pygame.K_w])
        
        # Dash
        if p["dash_cd"] > 0: p["dash_cd"] -= dt
        if keys[pygame.K_SPACE] and p["dash_cd"] <= 0 and (input_x!=0 or input_y!=0):
            mag = math.hypot(input_x, input_y)
            p["vx"] = (input_x/mag) * 1200
            p["vy"] = (input_y/mag) * 1200
            p["dash_cd"] = p["dash_max"]
            self.shake += 5
            # Dash particles
            for _ in range(8):
                self.entities["particles"].append(Particle(p["x"], p["y"], random.uniform(-50,50), random.uniform(-50,50), COL_P, 0.5))

        p["vx"] += input_x * acc * dt
        p["vy"] += input_y * acc * dt
        p["vx"] -= p["vx"] * fric * dt
        p["vy"] -= p["vy"] * fric * dt
        
        p["x"] += p["vx"] * dt
        p["y"] += p["vy"] * dt
        p["x"] = max(20, min(W-20, p["x"]))
        p["y"] = max(20, min(H-20, p["y"]))

        # 3. Shooting
        mouse_pressed = pygame.mouse.get_pressed()[0]
        gun = self.guns[p["gun_idx"]]
        if mouse_pressed and not p["reloading"] and gun["cur"] > 0:
            now = time.time()
            if (gun["auto"] or not hasattr(self, 'prev_mouse') or not self.prev_mouse) and now - gun["last"] >= gun["cd"]:
                gun["last"] = now
                gun["cur"] -= 1
                self.shake += 3
                
                mx, my = pygame.mouse.get_pos()
                base_angle = math.atan2(my - p["y"], mx - p["x"])
                
                # Knockback player
                p["vx"] -= math.cos(base_angle) * 150
                p["vy"] -= math.sin(base_angle) * 150

                for _ in range(gun["pellets"]):
                    spread = math.radians(random.uniform(-gun["spread"], gun["spread"]))
                    angle = base_angle + spread
                    self.entities["bullets"].append({
                        "x": p["x"], "y": p["y"],
                        "vx": math.cos(angle) * gun["spd"],
                        "vy": math.sin(angle) * gun["spd"],
                        "life": 1.5, "dmg": gun["dmg"]
                    })
        self.prev_mouse = mouse_pressed

        # 4. Projectiles Logic
        for b in self.entities["bullets"][:]:
            b["x"] += b["vx"] * dt
            b["y"] += b["vy"] * dt
            b["life"] -= dt
            if b["life"] <= 0: 
                self.entities["bullets"].remove(b)
                continue
            
            # Hit Enemy
            for e in self.entities["enemies"][:]:
                dist = math.hypot(b["x"] - e["x"], b["y"] - e["y"])
                if dist < 20:
                    e["hp"] -= b["dmg"]
                    self.entities["texts"].append(FloatingText(e["x"], e["y"]-20, str(b["dmg"])))
                    self.entities["particles"].append(Particle(b["x"], b["y"], random.uniform(-100,100), random.uniform(-100,100), e["color"], 0.4))
                    
                    # Push enemy
                    e["vx"] += b["vx"] * 0.2
                    e["vy"] += b["vy"] * 0.2
                    
                    if b in self.entities["bullets"]: self.entities["bullets"].remove(b)
                    
                    if e["hp"] <= 0:
                        self.kill_enemy(e)
                    break
        
        # Enemy Bullets (Sniper shots)
        for b in self.entities["e_bullets"][:]:
            b["x"] += b["vx"] * dt
            b["y"] += b["vy"] * dt
            # Check player hit
            if math.hypot(b["x"]-p["x"], b["y"]-p["y"]) < 15:
                self.damage_player(15)
                self.entities["e_bullets"].remove(b)
            elif not (0 <= b["x"] <= W and 0 <= b["y"] <= H):
                self.entities["e_bullets"].remove(b)

        # 5. Enemies Logic
        for e in self.entities["enemies"][:]:
            # Physics (separation)
            for other in self.entities["enemies"]:
                if e == other: continue
                dx, dy = e["x"] - other["x"], e["y"] - other["y"]
                d = math.hypot(dx, dy)
                if d < 30 and d > 0:
                    e["vx"] += (dx/d) * 500 * dt
                    e["vy"] += (dy/d) * 500 * dt
            
            # AI
            dx, dy = p["x"] - e["x"], p["y"] - e["y"]
            dist = math.hypot(dx, dy)
            dir_x, dir_y = (dx/dist), (dy/dist) if dist > 0 else (0,0)
            
            if e["type"] == "grunt":
                e["vx"] += dir_x * e["spd"] * dt * 5
                e["vy"] += dir_y * e["spd"] * dt * 5
            
            elif e["type"] == "sniper":
                target_dist = 400
                if dist < target_dist: # Retreat
                    e["vx"] -= dir_x * e["spd"] * dt * 3
                    e["vy"] -= dir_y * e["spd"] * dt * 3
                else: # Approach
                    e["vx"] += dir_x * e["spd"] * dt * 3
                    e["vy"] += dir_y * e["spd"] * dt * 3
                
                e["atk_cd"] -= dt
                if e["atk_cd"] <= 0:
                    e["atk_cd"] = 3.0
                    # Fire sniper shot
                    self.entities["e_bullets"].append({
                        "x": e["x"], "y": e["y"],
                        "vx": dir_x * 400, "vy": dir_y * 400
                    })
            
            elif e["type"] == "bomber":
                e["vx"] += dir_x * e["spd"] * dt * 8
                e["vy"] += dir_y * e["spd"] * dt * 8
                # Explode if close
                if dist < 40:
                    self.damage_player(40)
                    self.shake = 20
                    self.kill_enemy(e) # Blows self up
                    continue

            # Apply velocity & Friction
            e["x"] += e["vx"] * dt
            e["y"] += e["vy"] * dt
            e["vx"] *= 0.9
            e["vy"] *= 0.9

            # Collision with Player
            if dist < 25 and e["type"] != "bomber":
                self.damage_player(30 * dt) # DPS contact damage

        # 6. Scraps (Magnet)
        for s in self.entities["scraps"][:]:
            dx, dy = p["x"] - s["x"], p["y"] - s["y"]
            dist = math.hypot(dx, dy)
            if dist < 100:
                s["x"] += (dx/dist) * 600 * dt
                s["y"] += (dy/dist) * 600 * dt
            if dist < 20:
                self.scrap += s["val"]
                self.entities["scraps"].remove(s)

        # 7. Check Wave End
        if not self.entities["enemies"]:
            self.state = "SHOP"

    def update_shop(self):
        # Input handled in event loop, just waiting here
        pass

    def damage_player(self, amount):
        self.p["hp"] -= amount
        self.shake += 5
        if self.p["hp"] <= 0:
            self.state = "GAMEOVER"

    def kill_enemy(self, e):
        if e in self.entities["enemies"]: 
            self.entities["enemies"].remove(e)
            # Spawn Scrap
            val = 5 if e["type"]=="grunt" else 10
            self.entities["scraps"].append({"x": e["x"], "y": e["y"], "val": val})
            # Death Particles
            for _ in range(8):
                self.entities["particles"].append(Particle(e["x"], e["y"], random.uniform(-60,60), random.uniform(-60,60), e["color"], 0.6))

    # ================= DRAW =================

    def draw(self):
        # Handle Shake offset
        off_x = random.uniform(-self.shake, self.shake)
        off_y = random.uniform(-self.shake, self.shake)
        
        self.display.fill(COL_BG)
        
        # Grid
        for x in range(0, W, 50): pygame.draw.line(self.display, COL_GRID, (x,0), (x,H))
        for y in range(0, H, 50): pygame.draw.line(self.display, COL_GRID, (0,y), (W,y))
        
        # Scraps
        for s in self.entities["scraps"]:
            pygame.draw.circle(self.display, COL_SCRAP, (int(s["x"]), int(s["y"])), 5)

        # Enemies
        for e in self.entities["enemies"]:
            # Draw flash if bomber
            col = e["color"]
            if e["type"] == "bomber" and (time.time() % 0.2 < 0.1): col = (255, 100, 100)
            pygame.draw.circle(self.display, col, (int(e["x"]), int(e["y"])), 15)
            # Health bar above enemy
            if e["hp"] < e["max_hp"]:
                pygame.draw.rect(self.display, (255,0,0), (e["x"]-15, e["y"]-25, 30, 4))
                pygame.draw.rect(self.display, (0,255,0), (e["x"]-15, e["y"]-25, 30*(e["hp"]/e["max_hp"]), 4))

        # Player
        px, py = int(self.p["x"]), int(self.p["y"])
        pygame.draw.circle(self.display, COL_P, (px, py), 15)
        
        # Weapons (Visual Aim Line)
        mx, my = pygame.mouse.get_pos()
        angle = math.atan2(my - self.p["y"], mx - self.p["x"])
        pygame.draw.line(self.display, COL_P, (px, py), (px + math.cos(angle)*25, py + math.sin(angle)*25), 3)

        # Bullets
        for b in self.entities["bullets"]:
            pygame.draw.circle(self.display, (255, 255, 150), (int(b["x"]), int(b["y"])), 3)
        for b in self.entities["e_bullets"]:
            pygame.draw.circle(self.display, (255, 50, 50), (int(b["x"]), int(b["y"])), 5)

        # Particles & Text
        for p in self.entities["particles"]: p.draw(self.display)
        for t in self.entities["texts"]:
            img = self.font_m.render(t.text, True, t.color)
            self.display.blit(img, (t.x - img.get_width()//2, t.y))

        # HUD
        self.draw_hud()

        if self.state == "SHOP": self.draw_shop_ui()
        if self.state == "GAMEOVER": self.draw_gameover()

        # Blit to screen with shake
        self.screen.blit(self.display, (off_x, off_y))
        pygame.display.flip()

    def draw_hud(self):
        # HP Bar
        pygame.draw.rect(self.display, (50,0,0), (20, 20, 200, 20))
        pygame.draw.rect(self.display, (255,50,50), (20, 20, 200 * max(0, self.p["hp"]/self.p["max_hp"]), 20))
        pygame.draw.rect(self.display, (255,255,255), (20, 20, 200, 20), 2)
        
        # Scrap Count
        txt_scrap = self.font_m.render(f"SCRAP: {self.scrap}", True, COL_SCRAP)
        self.display.blit(txt_scrap, (20, 50))
        
        # Ammo
        g = self.guns[self.p["gun_idx"]]
        col = (255, 255, 255) if not self.p["reloading"] else (255, 0, 0)
        txt = f"{g['name']}: {g['cur']}/{g['mag']}"
        if self.p["reloading"]: txt = "RELOADING..."
        img = self.font_m.render(txt, True, col)
        self.display.blit(img, (20, H - 40))
        
        # Dash cooldown
        if self.p["dash_cd"] > 0:
            pct = self.p["dash_cd"] / self.p["dash_max"]
            pygame.draw.rect(self.display, (0, 200, 255), (self.p["x"]-20, self.p["y"]+25, 40*(1-pct), 4))

    def draw_shop_ui(self):
        overlay = pygame.Surface((W, H))
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        self.display.blit(overlay, (0,0))
        
        title = self.font_l.render("SHOP - WAVE COMPLETE", True, COL_SCRAP)
        self.display.blit(title, (W//2 - title.get_width()//2, 100))
        
        opts = [
            "[1] Repair 30 HP ($20)",
            "[2] Max HP +20   ($50)",
            "[3] Damage +10%  ($60)",
            "[SPACE] NEXT WAVE"
        ]
        
        for i, txt in enumerate(opts):
            color = (255, 255, 255)
            if "$20" in txt and self.scrap < 20: color = (100, 100, 100)
            if "$50" in txt and self.scrap < 50: color = (100, 100, 100)
            if "$60" in txt and self.scrap < 60: color = (100, 100, 100)
            
            r = self.font_m.render(txt, True, color)
            self.display.blit(r, (W//2 - 150, 250 + i*50))

    def draw_gameover(self):
        overlay = pygame.Surface((W, H))
        overlay.set_alpha(230)
        overlay.fill((20,0,0))
        self.display.blit(overlay, (0,0))
        
        t1 = self.font_l.render("YOU DIED", True, (255,0,0))
        t2 = self.font_m.render(f"Reached Wave {self.wave}", True, (200,200,200))
        t3 = self.font_s.render("Press [R] to Restart", True, (255,255,255))
        
        self.display.blit(t1, (W//2 - t1.get_width()//2, H//2 - 50))
        self.display.blit(t2, (W//2 - t2.get_width()//2, H//2 + 10))
        self.display.blit(t3, (W//2 - t3.get_width()//2, H//2 + 60))

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if self.state == "GAMEOVER" and event.key == pygame.K_r:
                        self.reset_game()
                    
                    elif self.state == "SHOP":
                        if event.key == pygame.K_1 and self.scrap >= 20:
                            self.scrap -= 20
                            self.p["hp"] = min(self.p["hp"] + 30, self.p["max_hp"])
                        elif event.key == pygame.K_2 and self.scrap >= 50:
                            self.scrap -= 50
                            self.p["max_hp"] += 20
                            self.p["hp"] += 20
                        elif event.key == pygame.K_3 and self.scrap >= 60:
                            self.scrap -= 60
                            for g in self.guns: g["dmg"] *= 1.1
                        elif event.key == pygame.K_SPACE:
                            self.wave += 1
                            self.start_wave()

            self.update(dt)
            self.draw()

if __name__ == "__main__":
    Game().run()