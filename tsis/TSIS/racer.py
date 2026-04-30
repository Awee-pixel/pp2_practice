import pygame
import random
import math
from ui import CAR_COLORS, DIFFICULTY_SPEEDS

# ── colours ───────────────────────────────────────────────────────────────────
BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
GRAY    = (180, 180, 180)
DARK    = (30,  30,  30)
RED     = (220, 50,  50)
GREEN   = (50,  200, 80)
BLUE    = (50,  120, 220)
YELLOW  = (240, 200, 30)
ORANGE  = (255, 140, 0)
CYAN    = (0,   220, 220)
PURPLE  = (160, 60,  220)
ROAD_DARK  = (55,  55,  55)
ROAD_LINE  = (220, 220, 220)
GRASS_COL  = (40,  120, 40)

# ── layout constants ──────────────────────────────────────────────────────────
ROAD_LEFT  = 100
ROAD_RIGHT = 500
NUM_LANES  = 4
LANE_W     = (ROAD_RIGHT - ROAD_LEFT) // NUM_LANES

def lane_center(lane):
    return ROAD_LEFT + LANE_W * lane + LANE_W // 2

# ── drawing helpers ───────────────────────────────────────────────────────────
def draw_car(surf, cx, cy, w, h, color, is_enemy=False):
    body = pygame.Rect(cx - w//2, cy - h//2, w, h)
    pygame.draw.rect(surf, color, body, border_radius=6)
    # windshield
    ws_col = (180,220,255) if not is_enemy else (255,180,180)
    ws = pygame.Rect(cx - w//2 + 4, cy - h//2 + 6, w - 8, h//4)
    pygame.draw.rect(surf, ws_col, ws, border_radius=3)
    # wheels
    wh_col = (30, 30, 30)
    for wx, wy in [(-w//2-3, -h//3), (w//2-3, -h//3),
                   (-w//2-3,  h//4), (w//2-3,  h//4)]:
        pygame.draw.rect(surf, wh_col, (cx+wx, cy+wy, 6, 10), border_radius=2)


class PlayerCar:
    W, H = 36, 60

    def __init__(self, color_name, W_screen, H_screen):
        self.color = CAR_COLORS.get(color_name, CAR_COLORS["red"])
        self.lane  = 1                # 0-3
        self.x     = float(lane_center(self.lane))
        self.y     = float(H_screen - 100)
        self.target_x = self.x
        self.speed = 6.0              # base scroll speed (set externally)
        self.shield   = False
        self.nitro    = False
        self.nitro_timer = 0
        self.shield_timer = 0
        self.invincible_timer = 0     # brief grace after hit

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.target_x = float(lane_center(self.lane))

    def move_right(self):
        if self.lane < NUM_LANES - 1:
            self.lane += 1
            self.target_x = float(lane_center(self.lane))

    def update(self, dt):
        # smooth lane slide
        dx = self.target_x - self.x
        self.x += dx * 0.25
        # timers
        if self.nitro_timer > 0:
            self.nitro_timer -= 1
            if self.nitro_timer <= 0:
                self.nitro = False
        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield = False
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def activate_nitro(self, frames=180):
        self.nitro = True
        self.nitro_timer = frames

    def activate_shield(self, frames=9999):
        self.shield = True
        self.shield_timer = frames

    @property
    def rect(self):
        return pygame.Rect(int(self.x) - self.W//2, int(self.y) - self.H//2, self.W, self.H)

    def draw(self, surf):
        draw_car(surf, int(self.x), int(self.y), self.W, self.H, self.color)
        if self.shield:
            r = max(self.W, self.H)//2 + 6
            pygame.draw.circle(surf, CYAN, (int(self.x), int(self.y)), r, 3)
        if self.nitro:
            # flame
            for i in range(3):
                ox = random.randint(-6, 6)
                fy = int(self.y) + self.H//2 + random.randint(4, 18)
                pygame.draw.circle(surf, ORANGE, (int(self.x)+ox, fy), random.randint(4,8))


class TrafficCar:
    W, H = 36, 60
    COLORS = [(180,180,180),(100,180,100),(180,100,100),(100,100,180),(230,180,50)]

    def __init__(self, lane, y, speed):
        self.lane  = lane
        self.x     = float(lane_center(lane))
        self.y     = float(y)
        self.speed = speed
        self.color = random.choice(self.COLORS)
        self.active = True

    def update(self, scroll_speed):
        self.y += self.speed + scroll_speed * 0.4
        if self.y > 700:
            self.active = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x) - self.W//2, int(self.y) - self.H//2, self.W, self.H)

    def draw(self, surf):
        draw_car(surf, int(self.x), int(self.y), self.W, self.H, self.color, is_enemy=True)


class Obstacle:
    """Oil spill, pothole, or speed bump."""
    TYPES = ["oil", "pothole", "bump", "barrier"]
    TYPE_COLORS = {
        "oil":     (20,  20,  20),
        "pothole": (90,  60,  30),
        "bump":    (220, 160, 0),
        "barrier": (220, 50,  50),
    }

    def __init__(self, lane, y):
        self.lane   = lane
        self.x      = float(lane_center(lane))
        self.y      = float(y)
        self.kind   = random.choice(self.TYPES)
        self.active = True
        self.w      = LANE_W - 8
        self.h      = 24 if self.kind != "barrier" else 18

    def update(self, scroll_speed):
        self.y += scroll_speed
        if self.y > 700:
            self.active = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x) - self.w//2, int(self.y) - self.h//2, self.w, self.h)

    def draw(self, surf):
        col = self.TYPE_COLORS[self.kind]
        if self.kind == "oil":
            pygame.draw.ellipse(surf, col, self.rect)
            pygame.draw.ellipse(surf, (40,40,80), self.rect, 2)
        elif self.kind == "pothole":
            pygame.draw.ellipse(surf, col, self.rect)
            pygame.draw.ellipse(surf, (60,40,20), self.rect, 2)
        elif self.kind == "bump":
            pygame.draw.rect(surf, col, self.rect, border_radius=4)
            lbl = pygame.font.SysFont(None, 18).render("BUMP", True, BLACK)
            surf.blit(lbl, lbl.get_rect(center=self.rect.center))
        elif self.kind == "barrier":
            pygame.draw.rect(surf, col, self.rect, border_radius=3)
            stripe_col = WHITE
            for sx in range(self.rect.left, self.rect.right, 14):
                pygame.draw.line(surf, stripe_col,
                                 (sx, self.rect.top), (min(sx+7, self.rect.right), self.rect.bottom), 3)


class NitroStrip:
    """Speed boost strip on the road."""
    def __init__(self, lane, y):
        self.lane   = lane
        self.x      = float(lane_center(lane))
        self.y      = float(y)
        self.w      = LANE_W - 4
        self.h      = 20
        self.active = True
        self.timer  = 0

    def update(self, scroll_speed):
        self.y += scroll_speed
        self.timer += 1
        if self.y > 700:
            self.active = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x) - self.w//2, int(self.y) - self.h//2, self.w, self.h)

    def draw(self, surf):
        alpha = int(180 + 60 * math.sin(self.timer * 0.15))
        col = (min(255, alpha), 140, 0)
        pygame.draw.rect(surf, col, self.rect, border_radius=3)
        lbl = pygame.font.SysFont(None, 18).render("NITRO", True, WHITE)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))


class PowerUp:
    TYPES   = ["nitro", "shield", "repair"]
    COLORS  = {"nitro": ORANGE, "shield": CYAN, "repair": GREEN}
    SYMBOLS = {"nitro": "N", "shield": "S", "repair": "+"}
    LIFE    = 300  # frames before disappearing

    def __init__(self, lane, y):
        self.lane   = lane
        self.x      = float(lane_center(lane))
        self.y      = float(y)
        self.kind   = random.choice(self.TYPES)
        self.active = True
        self.age    = 0
        self.r      = 18

    def update(self, scroll_speed):
        self.y   += scroll_speed
        self.age += 1
        if self.y > 700 or self.age > self.LIFE:
            self.active = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x) - self.r, int(self.y) - self.r, self.r*2, self.r*2)

    def draw(self, surf):
        blink = (self.age > self.LIFE - 60) and (self.age % 10 < 5)
        if blink:
            return
        col = self.COLORS[self.kind]
        pygame.draw.circle(surf, col, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y)), self.r, 2)
        sym_fnt = pygame.font.SysFont(None, 26, bold=True)
        lbl = sym_fnt.render(self.SYMBOLS[self.kind], True, WHITE)
        surf.blit(lbl, lbl.get_rect(center=(int(self.x), int(self.y))))


class Coin:
    VALUES      = [1, 2, 5]
    WEIGHTS     = [60, 30, 10]
    VALUE_COLORS = {1: YELLOW, 2: ORANGE, 5: PURPLE}
    LIFE        = 400

    def __init__(self, lane, y):
        self.lane   = lane
        self.x      = float(lane_center(lane))
        self.y      = float(y)
        self.value  = random.choices(self.VALUES, self.WEIGHTS)[0]
        self.active = True
        self.age    = 0
        self.r      = 12

    def update(self, scroll_speed):
        self.y   += scroll_speed
        self.age += 1
        if self.y > 700 or self.age > self.LIFE:
            self.active = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x)-self.r, int(self.y)-self.r, self.r*2, self.r*2)

    def draw(self, surf):
        col = self.VALUE_COLORS[self.value]
        pygame.draw.circle(surf, col, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y)), self.r, 2)
        fnt = pygame.font.SysFont(None, 18, bold=True)
        lbl = fnt.render(str(self.value), True, BLACK)
        surf.blit(lbl, lbl.get_rect(center=(int(self.x), int(self.y))))


# ── road rendering ────────────────────────────────────────────────────────────
class Road:
    DASHES  = 12   # number of dashes per lane divider
    DASH_H  = 40
    GAP_H   = 30

    def __init__(self, H_screen):
        self.H      = H_screen
        self.offset = 0.0

    def update(self, speed):
        self.offset = (self.offset + speed) % (self.DASH_H + self.GAP_H)

    def draw(self, surf):
        W = surf.get_width()
        # grass
        surf.fill(GRASS_COL)
        # road body
        pygame.draw.rect(surf, ROAD_DARK, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, self.H))
        # lane dividers
        for l in range(1, NUM_LANES):
            lx = ROAD_LEFT + LANE_W * l
            y  = -self.offset
            while y < self.H:
                pygame.draw.rect(surf, ROAD_LINE, (lx - 2, y, 4, self.DASH_H))
                y += self.DASH_H + self.GAP_H
        # road edges
        pygame.draw.rect(surf, WHITE, (ROAD_LEFT - 4, 0, 4, self.H))
        pygame.draw.rect(surf, WHITE, (ROAD_RIGHT, 0, 4, self.H))


# ── HUD ───────────────────────────────────────────────────────────────────────
def draw_hud(surf, font_med, font_sm, score, coins, distance, finish_dist,
             active_powerup, powerup_timer, speed_mult, crash_count):
    W = surf.get_width()
    # semi-transparent panel
    panel = pygame.Surface((94, 180), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 140))
    surf.blit(panel, (4, 4))

    y = 8
    for txt, col in [
        (f"Score  {score}",  YELLOW),
        (f"Coins  {coins}",  ORANGE),
        (f"Dist   {int(distance)}m", CYAN),
        (f"Left   {max(0,int(finish_dist-distance))}m", GREEN),
    ]:
        lbl = font_sm.render(txt, True, col)
        surf.blit(lbl, (8, y))
        y += 26

    if active_powerup:
        secs = powerup_timer // 60
        col  = {"nitro": ORANGE, "shield": CYAN, "repair": GREEN}.get(active_powerup, WHITE)
        lbl  = font_sm.render(f"[{active_powerup.upper()}] {secs}s", True, col)
        surf.blit(lbl, (8, y))

    # speed indicator (right side)
    spd_txt = f"x{speed_mult:.1f}" if speed_mult > 1 else ""
    if spd_txt:
        lbl = font_med.render(spd_txt, True, ORANGE)
        surf.blit(lbl, (W - 60, 8))


# ── main GameSession ──────────────────────────────────────────────────────────
class GameSession:
    FINISH_DISTANCE = 3000  # metres to finish

    def __init__(self, settings, W, H):
        self.W, self.H = W, H
        self.settings  = settings
        diff = settings.get("difficulty", "normal")
        self.base_speed = DIFFICULTY_SPEEDS.get(diff, 6)

        self.player    = PlayerCar(settings.get("car_color","red"), W, H)
        self.player.speed = self.base_speed
        self.road      = Road(H)

        self.coins     = []
        self.powerups  = []
        self.traffic   = []
        self.obstacles = []
        self.nitro_strips = []

        self.score          = 0
        self.coin_count     = 0
        self.distance       = 0.0
        self.frame          = 0
        self.crash_count    = 0
        self.game_over      = False
        self.scroll_speed   = float(self.base_speed)
        self.speed_mult     = 1.0
        self.active_powerup = None
        self.powerup_timer  = 0

        # coin milestone for speed scaling
        self.coins_collected = 0

        # spawn intervals
        self.coin_interval    = 60
        self.traffic_interval = 120
        self.obs_interval     = 150
        self.pu_interval      = 300
        self.strip_interval   = 400

    # ── per-frame update ──────────────────────────────────────────────────────
    def update(self, keys):
        if self.game_over:
            return

        self.frame += 1

        # player input
        if keys[pygame.K_LEFT]  and self.frame % 8 == 0:
            self.player.move_left()
        if keys[pygame.K_RIGHT] and self.frame % 8 == 0:
            self.player.move_right()

        # compute speed
        nitro_boost = 1.5 if self.player.nitro else 1.0
        self.speed_mult  = nitro_boost
        self.scroll_speed = self.base_speed * nitro_boost

        # difficulty: speed ramps every 500m
        ramp = 1.0 + (self.distance // 500) * 0.08
        self.scroll_speed *= min(ramp, 2.5)

        self.road.update(self.scroll_speed)
        self.player.update(1)
        self.distance += self.scroll_speed / 60.0  # approx metres

        # powerup timer
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0 and self.active_powerup not in (None, "shield"):
                self.active_powerup = None

        # spawning
        self._spawn(self.frame)

        # update entities
        for lst in [self.coins, self.powerups, self.traffic, self.obstacles, self.nitro_strips]:
            for e in lst:
                e.update(self.scroll_speed)

        # prune dead
        for attr in ["coins","powerups","traffic","obstacles","nitro_strips"]:
            setattr(self, attr, [e for e in getattr(self, attr) if e.active])

        # collisions
        self._check_collisions()

        # finish
        if self.distance >= self.FINISH_DISTANCE:
            self.score += 500
            self.game_over = True

    def _spawn(self, f):
        # coins
        if f % max(20, self.coin_interval - int(self.distance//200)) == 0:
            lane = random.randint(0, NUM_LANES-1)
            self.coins.append(Coin(lane, -40))

        # traffic
        interval = max(40, self.traffic_interval - int(self.distance//100)*3)
        if f % interval == 0:
            lane  = random.randint(0, NUM_LANES-1)
            spd   = random.uniform(2, 4) + self.distance/800
            t     = TrafficCar(lane, -70, spd)
            # safe spawn
            if not any(abs(tr.x - t.x) < 50 and abs(tr.y - t.y) < 80 for tr in self.traffic):
                self.traffic.append(t)

        # obstacles
        obs_interval = max(60, self.obs_interval - int(self.distance//150)*5)
        if f % obs_interval == 0:
            lane = random.randint(0, NUM_LANES-1)
            self.obstacles.append(Obstacle(lane, -30))

        # power-ups
        if f % self.pu_interval == 0:
            lane = random.randint(0, NUM_LANES-1)
            self.powerups.append(PowerUp(lane, -40))

        # nitro strips
        if f % self.strip_interval == 0:
            lane = random.randint(0, NUM_LANES-1)
            self.nitro_strips.append(NitroStrip(lane, -30))

    def _check_collisions(self):
        pr = self.player.rect

        # coins
        for c in self.coins:
            if pr.colliderect(c.rect):
                self.score          += c.value * 10
                self.coin_count     += c.value
                self.coins_collected += c.value
                c.active = False
                # speed up enemies after milestones
                if self.coins_collected % 10 == 0:
                    for t in self.traffic:
                        t.speed = min(t.speed + 0.5, 10)

        # power-ups
        for p in self.powerups:
            if pr.colliderect(p.rect):
                p.active = False
                self._apply_powerup(p.kind)

        # nitro strips
        for ns in self.nitro_strips:
            if pr.colliderect(ns.rect):
                ns.active = False
                self.player.activate_nitro(180)
                self.active_powerup = "nitro"
                self.powerup_timer  = 180

        # traffic collision
        if self.player.invincible_timer <= 0:
            for t in self.traffic:
                if pr.colliderect(t.rect):
                    self._handle_collision(t)

        # obstacle collision
        if self.player.invincible_timer <= 0:
            for o in self.obstacles:
                if pr.colliderect(o.rect):
                    self._handle_collision(o)

    def _apply_powerup(self, kind):
        self.active_powerup = kind
        if kind == "nitro":
            self.player.activate_nitro(180)
            self.powerup_timer = 180
        elif kind == "shield":
            self.player.activate_shield()
            self.powerup_timer = 9999
        elif kind == "repair":
            self.crash_count = max(0, self.crash_count - 1)
            self.score += 50
            self.powerup_timer = 120
            self.active_powerup = "repair"

    def _handle_collision(self, obj):
        if self.player.shield:
            # shield absorbs one hit
            obj.active = False
            self.player.shield      = False
            self.player.shield_timer = 0
            self.active_powerup = None
            self.player.invincible_timer = 90
        else:
            obj.active = False
            self.crash_count += 1
            self.player.invincible_timer = 90
            self.score = max(0, self.score - 30)
            if self.crash_count >= 3:
                self.game_over = True

    # ── draw ──────────────────────────────────────────────────────────────────
    def draw(self, surf, font_med, font_sm):
        self.road.draw(surf)

        for ns in self.nitro_strips:
            ns.draw(surf)
        for o in self.obstacles:
            o.draw(surf)
        for c in self.coins:
            c.draw(surf)
        for p in self.powerups:
            p.draw(surf)
        for t in self.traffic:
            t.draw(surf)

        # blink player on invincible frames
        if self.player.invincible_timer == 0 or (self.player.invincible_timer // 6) % 2 == 0:
            self.player.draw(surf)

        # crash hearts
        for i in range(3):
            col = RED if i < (3 - self.crash_count) else (60, 60, 60)
            pygame.draw.circle(surf, col, (self.W - 30 - i*28, 30), 10)

        draw_hud(surf, font_med, font_sm,
                 self.score, self.coin_count, self.distance,
                 self.FINISH_DISTANCE,
                 self.active_powerup, self.powerup_timer,
                 self.speed_mult, self.crash_count)
