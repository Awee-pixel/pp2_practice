import pygame
import sys
import time

from persistence import load_settings, save_settings, load_leaderboard, add_score
from racer import GameSession
from ui import (draw_main_menu, draw_username_screen, draw_settings,
                draw_leaderboard, draw_game_over)

# ── window ────────────────────────────────────────────────────────────────────
W, H = 600, 650
FPS  = 60

# ── states ────────────────────────────────────────────────────────────────────
MENU        = "menu"
USERNAME    = "username"
PLAYING     = "playing"
GAME_OVER   = "game_over"
LEADERBOARD = "leaderboard"
SETTINGS    = "settings"


def main():
    pygame.init()
    pygame.mixer.init()
    surf = pygame.display.set_mode((W, H))
    pygame.display.set_caption("RACER — TSIS 3")
    clock = pygame.time.Clock()

    pygame.mixer.music.load("music.mp3") 
    pygame.mixer.music.play(-1) # -1 значит, что музыка будет играть бесконечно
   

    font_big = pygame.font.SysFont(None, 72, bold=True)
    font_med = pygame.font.SysFont(None, 36)
    font_sm  = pygame.font.SysFont(None, 26)

    settings   = load_settings()
    state      = MENU
    session    = None
    username   = ""
    cursor_vis = True
    cursor_t   = time.time()

    while True:
        clock.tick(FPS)
        if settings.get("sound", True):
            pygame.mixer.music.set_volume(0.5) 
        else:
            pygame.mixer.music.set_volume(0.0)
        mouse_pos = pygame.mouse.get_pos()
        dt = clock.get_time()

        # ── events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ── MENU ──────────────────────────────────────────────────────────
            if state == MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    btns = draw_main_menu(surf, font_big, font_med, mouse_pos)
                    if btns["play"].collidepoint(mouse_pos):
                        state = USERNAME
                    elif btns["leaderboard"].collidepoint(mouse_pos):
                        state = LEADERBOARD
                    elif btns["settings"].collidepoint(mouse_pos):
                        state = SETTINGS
                    elif btns["quit"].collidepoint(mouse_pos):
                        pygame.quit(); sys.exit()

            # ── USERNAME ──────────────────────────────────────────────────────
            elif state == USERNAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and username.strip():
                        session = GameSession(settings, W, H)
                        state = PLAYING
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 16 and event.unicode.isprintable():
                            username += event.unicode

            # ── PLAYING ───────────────────────────────────────────────────────
            elif state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = MENU

            # ── GAME OVER ─────────────────────────────────────────────────────
            elif state == GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    btns = draw_game_over(surf, font_big, font_med,
                                         session.score, session.distance,
                                         session.coin_count, mouse_pos)
                    if btns["retry"].collidepoint(mouse_pos):
                        session = GameSession(settings, W, H)
                        state = PLAYING
                    elif btns["menu"].collidepoint(mouse_pos):
                        state = MENU

            # ── LEADERBOARD ───────────────────────────────────────────────────
            elif state == LEADERBOARD:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    entries = load_leaderboard()
                    btns = draw_leaderboard(surf, font_big, font_med, font_sm,
                                            entries, mouse_pos)
                    if btns["back"].collidepoint(mouse_pos):
                        state = MENU

            # ── SETTINGS ──────────────────────────────────────────────────────
            elif state == SETTINGS:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    btns = draw_settings(surf, font_big, font_med, settings, mouse_pos)
                    for key, rect in btns.items():
                        if rect.collidepoint(mouse_pos):
                            if key == "sound_on":
                                settings["sound"] = True
                            elif key == "sound_off":
                                settings["sound"] = False
                            elif key.startswith("color_"):
                                settings["car_color"] = key[6:]
                            elif key.startswith("diff_"):
                                settings["difficulty"] = key[5:]
                            elif key == "back":
                                save_settings(settings)
                                state = MENU

        # ── cursor blink ──────────────────────────────────────────────────────
        if time.time() - cursor_t > 0.5:
            cursor_vis = not cursor_vis
            cursor_t   = time.time()

        # ── update game ───────────────────────────────────────────────────────
        if state == PLAYING:
            keys = pygame.key.get_pressed()
            session.update(keys)
            if session.game_over:
                # save to leaderboard
                add_score(username or "Player", session.score,
                          session.distance, session.coin_count)
                state = GAME_OVER

        # ── draw ──────────────────────────────────────────────────────────────
        if state == MENU:
            draw_main_menu(surf, font_big, font_med, mouse_pos)

        elif state == USERNAME:
            draw_username_screen(surf, font_big, font_med, username, cursor_vis)

        elif state == PLAYING:
            session.draw(surf, font_med, font_sm)

        elif state == GAME_OVER:
            draw_game_over(surf, font_big, font_med,
                           session.score, session.distance,
                           session.coin_count, mouse_pos)

        elif state == LEADERBOARD:
            entries = load_leaderboard()
            draw_leaderboard(surf, font_big, font_med, font_sm, entries, mouse_pos)

        elif state == SETTINGS:
            draw_settings(surf, font_big, font_med, settings, mouse_pos)

        pygame.display.flip()


if __name__ == "__main__":
    main()
