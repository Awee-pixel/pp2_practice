import pygame

# ── colours ──────────────────────────────────────────────────────────────────
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
ROAD_DARK  = (60,  60,  60)
ROAD_LIGHT = (80,  80,  80)
LANE_WHITE = (230, 230, 230)
GRASS   = (40,  120, 40)

CAR_COLORS = {
    "red":    (220, 50,  50),
    "blue":   (50,  120, 220),
    "green":  (50,  200, 80),
    "yellow": (240, 200, 30),
    "purple": (160, 60,  220),
}

DIFFICULTY_SPEEDS = {"easy": 4, "normal": 6, "hard": 9}

# ── helper ────────────────────────────────────────────────────────────────────
def draw_button(surf, rect, text, font, bg=DARK, fg=WHITE, border=GRAY, hover=False):
    color = (60, 60, 60) if hover else bg
    pygame.draw.rect(surf, color, rect, border_radius=8)
    pygame.draw.rect(surf, border, rect, 2, border_radius=8)
    lbl = font.render(text, True, fg)
    surf.blit(lbl, lbl.get_rect(center=rect.center))

def draw_text_center(surf, text, font, color, y):
    lbl = font.render(text, True, color)
    surf.blit(lbl, lbl.get_rect(centerx=surf.get_width()//2, y=y))

# ── screens ───────────────────────────────────────────────────────────────────
def draw_main_menu(surf, font_big, font_med, mouse_pos):
    W, H = surf.get_size()
    surf.fill(DARK)
    # title
    draw_text_center(surf, "RACER", font_big, YELLOW, 80)
    draw_text_center(surf, "ARCADE", font_big, ORANGE, 140)

    buttons = {}
    labels = [("Play", GREEN), ("Leaderboard", CYAN), ("Settings", GRAY), ("Quit", RED)]
    for i, (lbl, col) in enumerate(labels):
        r = pygame.Rect(W//2 - 120, 240 + i*80, 240, 56)
        hover = r.collidepoint(mouse_pos)
        draw_button(surf, r, lbl, font_med, bg=(20,20,20), fg=col, hover=hover)
        buttons[lbl.lower()] = r
    return buttons

def draw_username_screen(surf, font_big, font_med, name_str, cursor_visible):
    W, H = surf.get_size()
    surf.fill(DARK)
    draw_text_center(surf, "Enter Your Name", font_big, YELLOW, 100)
    draw_text_center(surf, "Type your name and press ENTER", font_med, GRAY, 180)

    box = pygame.Rect(W//2 - 160, 240, 320, 56)
    pygame.draw.rect(surf, (40, 40, 40), box, border_radius=8)
    pygame.draw.rect(surf, YELLOW, box, 2, border_radius=8)
    display = name_str + ("|" if cursor_visible else "")
    lbl = font_med.render(display, True, WHITE)
    surf.blit(lbl, lbl.get_rect(midleft=(box.x + 12, box.centery)))

def draw_settings(surf, font_big, font_med, settings, mouse_pos):
    W, H = surf.get_size()
    surf.fill(DARK)
    draw_text_center(surf, "Settings", font_big, YELLOW, 60)

    buttons = {}

    # Sound toggle
    sy = 150
    draw_text_center(surf, "Sound", font_med, GRAY, sy)
    r_on  = pygame.Rect(W//2 - 130, sy+40, 120, 48)
    r_off = pygame.Rect(W//2 + 10,  sy+40, 120, 48)
    draw_button(surf, r_on,  "ON",  font_med,
                bg=(0,120,0) if settings["sound"] else DARK,
                fg=WHITE, hover=r_on.collidepoint(mouse_pos))
    draw_button(surf, r_off, "OFF", font_med,
                bg=(160,0,0) if not settings["sound"] else DARK,
                fg=WHITE, hover=r_off.collidepoint(mouse_pos))
    buttons["sound_on"]  = r_on
    buttons["sound_off"] = r_off

    # Car colour
    cy = 280
    draw_text_center(surf, "Car Color", font_med, GRAY, cy)
    col_names = list(CAR_COLORS.keys())
    for idx, cname in enumerate(col_names):
        rx = W//2 - (len(col_names)*66)//2 + idx*66
        r = pygame.Rect(rx, cy+40, 56, 48)
        sel = settings["car_color"] == cname
        pygame.draw.rect(surf, CAR_COLORS[cname], r, border_radius=6)
        if sel:
            pygame.draw.rect(surf, WHITE, r, 3, border_radius=6)
        buttons[f"color_{cname}"] = r

    # Difficulty
    dy = 410
    draw_text_center(surf, "Difficulty", font_med, GRAY, dy)
    diff_opts = ["easy", "normal", "hard"]
    diff_colors = [GREEN, YELLOW, RED]
    for idx, (d, dc) in enumerate(zip(diff_opts, diff_colors)):
        rx = W//2 - 210 + idx*145
        r = pygame.Rect(rx, dy+40, 130, 48)
        sel = settings["difficulty"] == d
        draw_button(surf, r, d.capitalize(), font_med,
                    bg=(40,40,40) if not sel else (60,60,60),
                    fg=dc, border=dc if sel else GRAY,
                    hover=r.collidepoint(mouse_pos))
        buttons[f"diff_{d}"] = r

    # Back
    rb = pygame.Rect(W//2 - 80, H - 80, 160, 52)
    draw_button(surf, rb, "Back", font_med, hover=rb.collidepoint(mouse_pos))
    buttons["back"] = rb
    return buttons

def draw_leaderboard(surf, font_big, font_med, font_sm, entries, mouse_pos):
    W, H = surf.get_size()
    surf.fill(DARK)
    draw_text_center(surf, "Top 10 Scores", font_big, YELLOW, 40)

    headers = ["#", "Name", "Score", "Dist(m)", "Coins"]
    col_x   = [40, 90, 280, 390, 490]
    # header row
    for txt, cx in zip(headers, col_x):
        lbl = font_sm.render(txt, True, GRAY)
        surf.blit(lbl, (cx, 110))
    pygame.draw.line(surf, GRAY, (30, 135), (W-30, 135), 1)

    for i, e in enumerate(entries[:10]):
        y = 150 + i * 42
        bg = (45, 45, 45) if i % 2 == 0 else (35, 35, 35)
        pygame.draw.rect(surf, bg, (30, y-4, W-60, 36), border_radius=4)
        row = [str(i+1), e.get("name","?")[:14], str(e.get("score",0)),
               str(e.get("distance",0)), str(e.get("coins",0))]
        colors = [ORANGE, WHITE, GREEN, CYAN, YELLOW]
        for txt, cx, col in zip(row, col_x, colors):
            lbl = font_sm.render(txt, True, col)
            surf.blit(lbl, (cx, y))

    rb = pygame.Rect(W//2 - 80, H - 70, 160, 52)
    draw_button(surf, rb, "Back", font_med, hover=rb.collidepoint(mouse_pos))
    return {"back": rb}

def draw_game_over(surf, font_big, font_med, score, distance, coins, mouse_pos):
    W, H = surf.get_size()
    surf.fill(DARK)
    draw_text_center(surf, "GAME OVER", font_big, RED, 80)

    stats = [
        ("Score",    str(score),      YELLOW),
        ("Distance", f"{int(distance)} m", CYAN),
        ("Coins",    str(coins),      GREEN),
    ]
    for i, (label, val, col) in enumerate(stats):
        y = 180 + i * 60
        draw_text_center(surf, f"{label}: {val}", font_med, col, y)

    buttons = {}
    r_retry = pygame.Rect(W//2 - 130, 380, 240, 56)
    r_menu  = pygame.Rect(W//2 - 130, 450, 240, 56)
    draw_button(surf, r_retry, "Retry",     font_med, fg=GREEN, hover=r_retry.collidepoint(mouse_pos))
    draw_button(surf, r_menu,  "Main Menu", font_med, fg=ORANGE, hover=r_menu.collidepoint(mouse_pos))
    buttons["retry"] = r_retry
    buttons["menu"]  = r_menu
    return buttons
