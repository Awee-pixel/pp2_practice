import pygame
import sys
import json
import os

from config import *
import db
from game import GameState


SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")


def load_settings() -> dict:
    try:
        with open(SETTINGS_FILE) as f:
            data = json.load(f)
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"[Settings] save error: {e}")


def draw_text_centered(surface, font, text, color, cx, cy):
    surf = font.render(text, True, color)
    surface.blit(surf, surf.get_rect(center=(cx, cy)))


def draw_button(surface, font, text, rect: pygame.Rect,
                bg=PANEL_BG, fg=ACCENT, hover=False):
    col = tuple(min(255, c + 30) for c in bg) if hover else bg
    pygame.draw.rect(surface, col, rect, border_radius=8)
    pygame.draw.rect(surface, fg, rect, 2, border_radius=8)
    draw_text_centered(surface, font, text, fg, rect.centerx, rect.centery)


def button_clicked(rect, events) -> bool:
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if rect.collidepoint(e.pos):
                return True
    return False

class App:
    SCREEN_MENU        = "menu"
    SCREEN_GAME        = "game"
    SCREEN_GAMEOVER    = "gameover"
    SCREEN_LEADERBOARD = "leaderboard"
    SCREEN_SETTINGS    = "settings"

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        self.screen  = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock   = pygame.time.Clock()
        pygame.mixer.music.load("music1.mp3") 
        pygame.mixer.music.play(-1)

        # Fonts
        self.font_xl  = pygame.font.SysFont("consolas", 48, bold=True)
        self.font_lg  = pygame.font.SysFont("consolas", 32, bold=True)
        self.font_md  = pygame.font.SysFont("consolas", 22)
        self.font_sm  = pygame.font.SysFont("consolas", 16)

        # State
        self.settings    = load_settings()
        self.db_ok       = db.init_db()

        self.screen_name = self.SCREEN_MENU
        self.username    = ""
        self.player_id: int | None = None
        self.personal_best = 0

        # game session (set when entering game screen)
        self.gs: GameState | None = None

        # last game result (for game-over screen)
        self.last_score = 0
        self.last_level = 1

        # leaderboard cache
        self._lb_rows: list[dict] = []

        # username input cursor blink
        self._cursor_visible = True
        self._cursor_timer   = 0

        # settings screen color picker state
        self._color_preview = list(self.settings["snake_color"])


    def run(self):
        while True:
            dt    = self.clock.tick(FPS)
            if self.settings.get("sound", True):
                pygame.mixer.music.set_volume(0.5) 
            else:
                pygame.mixer.music.set_volume(0.0)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(DARK_BG)

            if self.screen_name == self.SCREEN_MENU:
                self._update_menu(events, dt)
            elif self.screen_name == self.SCREEN_GAME:
                self._update_game(events, dt)
            elif self.screen_name == self.SCREEN_GAMEOVER:
                self._update_gameover(events)
            elif self.screen_name == self.SCREEN_LEADERBOARD:
                self._update_leaderboard(events)
            elif self.screen_name == self.SCREEN_SETTINGS:
                self._update_settings(events)

            pygame.display.flip()

    def _update_menu(self, events, dt):
        W, H = WINDOW_WIDTH, WINDOW_HEIGHT
        mx, my = pygame.mouse.get_pos()

        # cursor blink
        self._cursor_timer += dt
        if self._cursor_timer >= 530:
            self._cursor_timer   = 0
            self._cursor_visible = not self._cursor_visible

        # ── title ──
        draw_text_centered(self.screen, self.font_xl, "🐍  SNAKE", ACCENT,
                           W // 2, 80)
        draw_text_centered(self.screen, self.font_sm,
                           "TSIS 4 — Database Edition", GRAY, W // 2, 130)

        # DB status badge
        badge_col = ACCENT if self.db_ok else RED
        badge_txt = "● DB connected" if self.db_ok else "● DB offline"
        draw_text_centered(self.screen, self.font_sm, badge_txt,
                           badge_col, W // 2, 158)

        # ── username input ──
        draw_text_centered(self.screen, self.font_md, "Enter username:",
                           LIGHT_GRAY, W // 2, 210)
        inp_rect = pygame.Rect(W // 2 - 160, 228, 320, 38)
        pygame.draw.rect(self.screen, PANEL_BG, inp_rect, border_radius=6)
        pygame.draw.rect(self.screen, ACCENT2, inp_rect, 2, border_radius=6)

        display_name = self.username
        if self._cursor_visible:
            display_name += "|"
        name_surf = self.font_md.render(display_name, True, WHITE)
        self.screen.blit(name_surf, (inp_rect.x + 8, inp_rect.y + 6))

        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif e.key == pygame.K_RETURN:
                    self._confirm_username()
                elif len(self.username) < 20 and e.unicode.isprintable():
                    self.username += e.unicode

        # ── buttons ──
        btn_w, btn_h = 200, 46
        cx = W // 2
        btns = [
            ("PLAY",        pygame.Rect(cx - btn_w//2, 295, btn_w, btn_h)),
            ("LEADERBOARD", pygame.Rect(cx - btn_w//2, 355, btn_w, btn_h)),
            ("SETTINGS",    pygame.Rect(cx - btn_w//2, 415, btn_w, btn_h)),
            ("QUIT",        pygame.Rect(cx - btn_w//2, 475, btn_w, btn_h)),
        ]
        for label, rect in btns:
            hover = rect.collidepoint(mx, my)
            draw_button(self.screen, self.font_md, label, rect, hover=hover)
            if button_clicked(rect, events):
                if label == "PLAY":
                    self._confirm_username()
                    self._start_game()
                elif label == "LEADERBOARD":
                    self._lb_rows = db.get_leaderboard() if self.db_ok else []
                    self.screen_name = self.SCREEN_LEADERBOARD
                elif label == "SETTINGS":
                    self._color_preview = list(self.settings["snake_color"])
                    self.screen_name = self.SCREEN_SETTINGS
                elif label == "QUIT":
                    pygame.quit()
                    sys.exit()

    def _confirm_username(self):
        name = self.username.strip() or "Anonymous"
        self.username = name
        if self.db_ok:
            self.player_id     = db.get_or_create_player(name)
            self.personal_best = db.get_personal_best(self.player_id) \
                                 if self.player_id else 0

    def _start_game(self):
        color = self.settings["snake_color"]
        pb    = self.personal_best
        self.gs          = GameState(color, personal_best=pb)
        self.screen_name = self.SCREEN_GAME

    def _update_game(self, events, dt):
        W = WINDOW_WIDTH
        gs = self.gs

        # input
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_UP,    pygame.K_w):
                    gs.snake.set_direction((0, -1))
                elif e.key in (pygame.K_DOWN,  pygame.K_s):
                    gs.snake.set_direction((0,  1))
                elif e.key in (pygame.K_LEFT,  pygame.K_a):
                    gs.snake.set_direction((-1, 0))
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    gs.snake.set_direction((1,  0))
                elif e.key == pygame.K_ESCAPE:
                    self.screen_name = self.SCREEN_MENU

        # update
        result = gs.update(dt)
        if result == "gameover":
            self._handle_gameover()
            return

        # ── HUD ──
        hud_rect = pygame.Rect(0, 0, W, HUD_HEIGHT)
        pygame.draw.rect(self.screen, PANEL_BG, hud_rect)
        pygame.draw.line(self.screen, ACCENT, (0, HUD_HEIGHT - 1),
                         (W, HUD_HEIGHT - 1), 1)

        # score / level / personal best
        self.screen.blit(self.font_md.render(f"SCORE  {gs.score}", True, WHITE),
                         (16, 10))
        self.screen.blit(self.font_md.render(f"LEVEL  {gs.level}", True, ACCENT2),
                         (16, 36))
        self.screen.blit(self.font_sm.render(f"BEST  {gs.personal_best}", True, GOLD),
                         (16, 60))

        # power-up status
        now = pygame.time.get_ticks()
        if gs.active_pu:
            remaining = max(0, gs.pu_end_ms - now) / 1000
            pu_txt = f"{PU_LABELS[gs.active_pu]}  {remaining:.1f}s"
            draw_text_centered(self.screen, self.font_md, pu_txt,
                               PU_COLORS[gs.active_pu], W // 2, 26)
        if gs.shield_active:
            draw_text_centered(self.screen, self.font_md, "🛡 SHIELD ACTIVE",
                               GOLD, W // 2, 52)

        # food legend (right side)
        legend_items = [
            (FOOD_COLORS[FOOD_NORMAL], "Normal  +10"),
            (FOOD_COLORS[FOOD_BONUS],  "Bonus   +30"),
            (FOOD_COLORS[FOOD_POISON], "Poison  -2 segs"),
        ]
        for i, (col, lbl) in enumerate(legend_items):
            x = W - 200
            y = 8 + i * 22
            pygame.draw.circle(self.screen, col, (x, y + 7), 6)
            self.screen.blit(self.font_sm.render(lbl, True, LIGHT_GRAY),
                             (x + 14, y))

        # speed bar
        spd_frac = min(1.0, (gs.level - 1) * SPEED_INC / 10)
        bar_w    = 120
        bar_x    = W // 2 - bar_w // 2
        pygame.draw.rect(self.screen, GRAY,
                         pygame.Rect(bar_x, HUD_HEIGHT - 14, bar_w, 8),
                         border_radius=4)
        pygame.draw.rect(self.screen, ACCENT,
                         pygame.Rect(bar_x, HUD_HEIGHT - 14,
                                     int(bar_w * spd_frac), 8),
                         border_radius=4)

        # ── Arena ──
        arena_y = HUD_HEIGHT
        pygame.draw.rect(self.screen, (10, 10, 20),
                         pygame.Rect(0, arena_y,
                                     COLS * CELL_SIZE, ROWS * CELL_SIZE))

        gs.draw(self.screen, arena_y,
                self.settings.get("grid_overlay", False), self.font_sm)

        # border
        pygame.draw.rect(self.screen, ACCENT,
                         pygame.Rect(0, arena_y,
                                     COLS * CELL_SIZE, ROWS * CELL_SIZE), 2)

    def _handle_gameover(self):
        gs = self.gs
        self.last_score = gs.score
        self.last_level = gs.level

        # save to DB
        if self.db_ok and self.player_id:
            db.save_session(self.player_id, gs.score, gs.level)
            self.personal_best = db.get_personal_best(self.player_id)

        self.screen_name = self.SCREEN_GAMEOVER


    def _update_gameover(self, events):
        W, H = WINDOW_WIDTH, WINDOW_HEIGHT
        mx, my = pygame.mouse.get_pos()

        # dim overlay on top of frozen arena
        if self.gs:
            self.gs.draw(self.screen, HUD_HEIGHT,
                         self.settings.get("grid_overlay", False), self.font_sm)
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # panel
        panel = pygame.Rect(W // 2 - 200, H // 2 - 180, 400, 360)
        pygame.draw.rect(self.screen, PANEL_BG, panel, border_radius=12)
        pygame.draw.rect(self.screen, RED, panel, 2, border_radius=12)

        draw_text_centered(self.screen, self.font_xl, "GAME OVER",
                           RED, W // 2, H // 2 - 130)
        draw_text_centered(self.screen, self.font_lg,
                           f"Score: {self.last_score}", WHITE,
                           W // 2, H // 2 - 70)
        draw_text_centered(self.screen, self.font_md,
                           f"Level reached: {self.last_level}", ACCENT2,
                           W // 2, H // 2 - 30)
        draw_text_centered(self.screen, self.font_md,
                           f"Personal best: {self.personal_best}", GOLD,
                           W // 2, H // 2 + 10)

        btn_w, btn_h = 160, 44
        retry_rect   = pygame.Rect(W // 2 - btn_w - 10, H // 2 + 60, btn_w, btn_h)
        menu_rect    = pygame.Rect(W // 2 + 10,           H // 2 + 60, btn_w, btn_h)

        draw_button(self.screen, self.font_md, "RETRY",     retry_rect,
                    hover=retry_rect.collidepoint(mx, my))
        draw_button(self.screen, self.font_md, "MAIN MENU", menu_rect,
                    hover=menu_rect.collidepoint(mx, my))

        if button_clicked(retry_rect, events):
            self._start_game()
        if button_clicked(menu_rect, events):
            self.screen_name = self.SCREEN_MENU


    def _update_leaderboard(self, events):
        W, H = WINDOW_WIDTH, WINDOW_HEIGHT
        mx, my = pygame.mouse.get_pos()

        draw_text_centered(self.screen, self.font_xl, "LEADERBOARD",
                           GOLD, W // 2, 50)

        if not self.db_ok:
            draw_text_centered(self.screen, self.font_md,
                               "Database not connected.", RED, W // 2, H // 2)
        else:
            # table header
            cols_x = [60, 160, 360, 480, 610]
            headers = ["#", "Username", "Score", "Level", "Date"]
            for hdr, x in zip(headers, cols_x):
                self.screen.blit(
                    self.font_sm.render(hdr, True, ACCENT),
                    (x, 110))
            pygame.draw.line(self.screen, ACCENT, (50, 130), (W - 50, 130), 1)

            for i, row in enumerate(self._lb_rows):
                y   = 140 + i * 30
                col = GOLD if i == 0 else (LIGHT_GRAY if i < 3 else GRAY)
                vals = [
                    str(row["rank"]),
                    row["username"][:14],
                    str(row["score"]),
                    str(row["level_reached"]),
                    row["played_at"].strftime("%m/%d %H:%M")
                    if row["played_at"] else "--",
                ]
                for val, x in zip(vals, cols_x):
                    self.screen.blit(
                        self.font_sm.render(val, True, col), (x, y))

        # back button
        back_rect = pygame.Rect(W // 2 - 80, H - 70, 160, 44)
        draw_button(self.screen, self.font_md, "BACK", back_rect,
                    hover=back_rect.collidepoint(mx, my))
        if button_clicked(back_rect, events):
            self.screen_name = self.SCREEN_MENU


    def _update_settings(self, events):
        W, H = WINDOW_WIDTH, WINDOW_HEIGHT
        mx, my = pygame.mouse.get_pos()

        draw_text_centered(self.screen, self.font_xl, "SETTINGS",
                           ACCENT2, W // 2, 50)

        # ── Grid overlay toggle ──
        grid_on = self.settings["grid_overlay"]
        grid_lbl = f"Grid overlay:  {'ON' if grid_on else 'OFF'}"
        grid_btn = pygame.Rect(W // 2 - 150, 130, 300, 44)
        draw_button(self.screen, self.font_md, grid_lbl, grid_btn,
                    fg=ACCENT if grid_on else GRAY,
                    hover=grid_btn.collidepoint(mx, my))
        if button_clicked(grid_btn, events):
            self.settings["grid_overlay"] = not grid_on

        # ── Sound toggle ──
        snd_on  = self.settings["sound"]
        snd_lbl = f"Sound:  {'ON' if snd_on else 'OFF'}"
        snd_btn = pygame.Rect(W // 2 - 150, 195, 300, 44)
        draw_button(self.screen, self.font_md, snd_lbl, snd_btn,
                    fg=ACCENT if snd_on else GRAY,
                    hover=snd_btn.collidepoint(mx, my))
        if button_clicked(snd_btn, events):
            self.settings["sound"] = not snd_on

        # ── Snake color presets ──
        draw_text_centered(self.screen, self.font_md, "Snake Color",
                           LIGHT_GRAY, W // 2, 280)
        presets = [
            ((0,  200, 100), "Green"),
            ((0,  170, 255), "Blue"),
            ((255, 80, 80),  "Red"),
            ((220, 180,  0), "Gold"),
            ((180,  0, 220), "Purple"),
        ]
        for i, (col, name) in enumerate(presets):
            bx = 120 + i * 115
            by = 300
            bw, bh = 90, 40
            rect = pygame.Rect(bx, by, bw, bh)
            selected = (tuple(self.settings["snake_color"]) == col)
            border_col = WHITE if selected else col
            pygame.draw.rect(self.screen, col, rect, border_radius=8)
            pygame.draw.rect(self.screen, border_col, rect, 3 if selected else 1,
                             border_radius=8)
            draw_text_centered(self.screen, self.font_sm, name, BLACK,
                               bx + bw//2, by + bh//2)
            if button_clicked(rect, events):
                self.settings["snake_color"] = list(col)

        # ── Preview ──
        preview_col = tuple(self.settings["snake_color"])
        pygame.draw.rect(self.screen, preview_col,
                         pygame.Rect(W // 2 - 30, 365, 60, 24), border_radius=6)
        draw_text_centered(self.screen, self.font_sm, "preview",
                           GRAY, W // 2, 405)

        # ── Save & Back ──
        save_rect = pygame.Rect(W // 2 - 100, H - 100, 200, 48)
        draw_button(self.screen, self.font_md, "SAVE & BACK", save_rect,
                    hover=save_rect.collidepoint(mx, my))
        if button_clicked(save_rect, events):
            save_settings(self.settings)
            self.screen_name = self.SCREEN_MENU

if __name__ == "__main__":
    App().run()
