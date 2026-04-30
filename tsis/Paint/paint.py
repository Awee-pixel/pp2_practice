import pygame
import sys
import math
import os
from datetime import datetime

from tools import (
    BRUSH_SIZES,
    TOOL_PENCIL, TOOL_LINE, TOOL_RECT, TOOL_CIRCLE,
    TOOL_SQUARE, TOOL_RTRI, TOOL_ETRI, TOOL_RHOMBUS,
    TOOL_FILL, TOOL_ERASER, TOOL_TEXT,
    flood_fill, draw_shape, TextSession,
)


WIN_W, WIN_H     = 1100, 760
TOOLBAR_W        = 200       # left panel width
CANVAS_X         = TOOLBAR_W
CANVAS_Y         = 0
CANVAS_W         = WIN_W - TOOLBAR_W
CANVAS_H         = WIN_H

# Palette
PALETTE = [
    (0,   0,   0),   (255, 255, 255), (200, 50,  50),  (230, 120, 40),
    (220, 200, 0),   (60,  180, 60),  (0,  180, 200),  (40,  90,  220),
    (140, 60,  200), (220, 60,  140), (160, 100, 60),   (120, 120, 120),
    (80,  200, 160), (255, 160, 80),  (255, 100, 100),  (100, 160, 255),
]

# UI colors (dark industrial theme — fits a utility app)
UI_BG        = (28,  30,  38)
UI_PANEL     = (36,  38,  50)
UI_BORDER    = (55,  60,  80)
UI_ACCENT    = (80, 180, 255)
UI_ACCENT2   = (0,  220, 140)
UI_TEXT      = (210, 215, 230)
UI_TEXT_DIM  = (120, 125, 145)
UI_SEL       = (60,  130, 210)
UI_HOVER     = (50,  55,  72)
UI_ERASER_FG = (180, 180, 200)

# Tool button layout
TOOL_ROWS = [
    [TOOL_PENCIL,  TOOL_LINE],
    [TOOL_RECT,    TOOL_CIRCLE],
    [TOOL_SQUARE,  TOOL_RTRI],
    [TOOL_ETRI,    TOOL_RHOMBUS],
    [TOOL_FILL,    TOOL_ERASER],
    [TOOL_TEXT,    None],
]

TOOL_LABELS = {
    TOOL_PENCIL:  "Pencil",
    TOOL_LINE:    "Line",
    TOOL_RECT:    "Rect",
    TOOL_CIRCLE:  "Circle",
    TOOL_SQUARE:  "Square",
    TOOL_RTRI:    "R.Tri",
    TOOL_ETRI:    "E.Tri",
    TOOL_RHOMBUS: "Rhombus",
    TOOL_FILL:    "Fill",
    TOOL_ERASER:  "Eraser",
    TOOL_TEXT:    "Text",
}

TOOL_ICONS = {
    TOOL_PENCIL:  "✏",
    TOOL_LINE:    "╱",
    TOOL_RECT:    "▭",
    TOOL_CIRCLE:  "◯",
    TOOL_SQUARE:  "□",
    TOOL_RTRI:    "◺",
    TOOL_ETRI:    "△",
    TOOL_RHOMBUS: "◇",
    TOOL_FILL:    "⬛",
    TOOL_ERASER:  "◻",
    TOOL_TEXT:    "T",
}

SAVE_DIR = os.path.join(os.path.dirname(__file__), "saves")


def draw_text(surf, font, text, color, x, y, anchor="topleft"):
    s = font.render(text, True, color)
    r = s.get_rect(**{anchor: (x, y)})
    surf.blit(s, r)


def is_hovered(rect):
    return rect.collidepoint(pygame.mouse.get_pos())


def clicked(rect, events, button=1):
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == button:
            if rect.collidepoint(e.pos):
                return True
    return False


class PaintApp:

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Paint — TSIS 2")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_ui   = pygame.font.SysFont("segoeui",    14, bold=False)
        self.font_bold = pygame.font.SysFont("segoeui",    14, bold=True)
        self.font_icon = pygame.font.SysFont("segoeuisymbol", 18)
        self.font_text = pygame.font.SysFont("consolas",   20)

        # Canvas
        self.canvas = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill((255, 255, 255))

        # Tool state
        self.active_tool   = TOOL_PENCIL
        self.brush_size_key = 1           # 1/2/3
        self.color         = (0, 0, 0)
        self.secondary_col = (255, 255, 255)  # right-click / eraser color

        # Drawing state
        self.drawing      = False
        self.start_pos    = None          # canvas-relative
        self.prev_pos     = None
        self.pencil_pts: list[tuple] = []

        # Preview layer (blit on top of canvas each frame while dragging)
        self.preview_surf = pygame.Surface((CANVAS_W, CANVAS_H), pygame.SRCALPHA)

        # Text session
        self.text_session: TextSession | None = None

        # Notification banner
        self._notif_text = ""
        self._notif_until = 0

        os.makedirs(SAVE_DIR, exist_ok=True)


    @property
    def brush_px(self) -> int:
        return BRUSH_SIZES[self.brush_size_key]


    def to_canvas(self, screen_pos):
        return (screen_pos[0] - CANVAS_X, screen_pos[1] - CANVAS_Y)

    def on_canvas(self, screen_pos):
        return (CANVAS_X <= screen_pos[0] < CANVAS_X + CANVAS_W and
                CANVAS_Y <= screen_pos[1] < CANVAS_Y + CANVAS_H)


    def save_canvas(self):
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = os.path.join(SAVE_DIR, f"canvas_{ts}.png")
        pygame.image.save(self.canvas, name)
        self._notify(f"Saved → saves/canvas_{ts}.png")

    def _notify(self, msg: str, ms: int = 2500):
        self._notif_text  = msg
        self._notif_until = pygame.time.get_ticks() + ms

    def run(self):
        while True:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self._handle_keys(events)
            self._handle_mouse(events)
            self._handle_text_events(events)
            self._draw_frame(events)
            self.clock.tick(60)

    def _handle_keys(self, events):
        for e in events:
            if e.type != pygame.KEYDOWN:
                continue
            mods = pygame.key.get_mods()

            # Ctrl+S → save
            if e.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                self.save_canvas()
                continue

            # Text tool input is handled separately
            if self.text_session:
                continue

            # Brush size 1/2/3
            if e.key == pygame.K_1:
                self.brush_size_key = 1
            elif e.key == pygame.K_2:
                self.brush_size_key = 2
            elif e.key == pygame.K_3:
                self.brush_size_key = 3

    def _handle_text_events(self, events):
        if not self.text_session:
            return
        for e in events:
            if e.type != pygame.KEYDOWN:
                continue
            # Don't let Ctrl+S steal events while typing
            mods = pygame.key.get_mods()
            if e.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                self.save_canvas()
                continue
            result = self.text_session.feed_event(e)
            if result == "confirm":
                self.text_session.commit(self.canvas)
                self.text_session = None
            elif result == "cancel":
                self.text_session = None

    def _handle_mouse(self, events):
        # Ignore if active text session
        if self.text_session:
            return

        mouse_pos = pygame.mouse.get_pos()

        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                btn = e.button
                if not self.on_canvas(e.pos):
                    continue

                cp = self.to_canvas(e.pos)
                draw_col = self.color if btn == 1 else self.secondary_col

                # ── fill ──
                if self.active_tool == TOOL_FILL:
                    flood_fill(self.canvas, cp[0], cp[1], draw_col)
                    continue

                # ── text placement ──
                if self.active_tool == TOOL_TEXT:
                    self.text_session = TextSession(
                        cp[0], cp[1], draw_col, self.font_text)
                    continue

                # ── start drag ──
                self.drawing   = True
                self.start_pos = cp
                self.prev_pos  = cp
                self.pencil_pts = [cp]

            elif e.type == pygame.MOUSEBUTTONUP:
                if not self.drawing:
                    continue
                self.drawing = False

                cp = self.to_canvas(e.pos)
                draw_col = (self.color if e.button == 1 else self.secondary_col)

                tool = self.active_tool

                if tool == TOOL_PENCIL or tool == TOOL_ERASER:
                    pass   # already drawn continuously in MOUSEMOTION
                elif tool in (TOOL_LINE, TOOL_RECT, TOOL_CIRCLE,
                              TOOL_SQUARE, TOOL_RTRI, TOOL_ETRI, TOOL_RHOMBUS):
                    draw_shape(tool, self.canvas, draw_col,
                               self.start_pos[0], self.start_pos[1],
                               cp[0], cp[1], self.brush_px)

                self.preview_surf.fill((0, 0, 0, 0))
                self.start_pos  = None
                self.pencil_pts = []

            elif e.type == pygame.MOUSEMOTION:
                if not self.drawing:
                    continue

                cp = self.to_canvas(e.pos)
                btn_held = pygame.mouse.get_pressed()
                draw_col = self.color if btn_held[0] else self.secondary_col
                tool     = self.active_tool
                sz       = self.brush_px

                if tool == TOOL_PENCIL:
                    if self.prev_pos:
                        pygame.draw.line(self.canvas, draw_col,
                                         self.prev_pos, cp, sz)
                    self.prev_pos = cp

                elif tool == TOOL_ERASER:
                    if self.prev_pos:
                        pygame.draw.line(self.canvas, self.secondary_col,
                                         self.prev_pos, cp,
                                         max(sz, 12))  # eraser is always chunkier
                    self.prev_pos = cp

                else:
                    # live preview for shape/line tools
                    self.preview_surf.fill((0, 0, 0, 0))
                    draw_shape(tool, self.preview_surf,
                               (*draw_col, 200),
                               self.start_pos[0], self.start_pos[1],
                               cp[0], cp[1], sz)


    def _handle_toolbar_clicks(self, events, rects: dict):
        # Tool buttons
        for tool, rect in rects.get("tools", {}).items():
            if tool and clicked(rect, events):
                self.active_tool  = tool
                self.text_session = None

        # Brush size buttons
        for sz_key, rect in rects.get("sizes", {}).items():
            if clicked(rect, events):
                self.brush_size_key = sz_key

        # Palette swatches
        for i, rect in enumerate(rects.get("palette", [])):
            if i >= len(PALETTE):
                break
            if clicked(rect, events, button=1):
                self.color = PALETTE[i]
            if clicked(rect, events, button=3):
                self.secondary_col = PALETTE[i]

        # Clear canvas
        if clicked(rects.get("clear", pygame.Rect(0, 0, 0, 0)), events):
            self.canvas.fill((255, 255, 255))
            self._notify("Canvas cleared")

        # Save button
        if clicked(rects.get("save", pygame.Rect(0, 0, 0, 0)), events):
            self.save_canvas()

    def _draw_frame(self, events):
        self.win.fill(UI_BG)

        # ── Canvas ──
        self.win.blit(self.canvas, (CANVAS_X, CANVAS_Y))

        if self.drawing and self.active_tool not in (TOOL_PENCIL, TOOL_ERASER,
                                                      TOOL_FILL, TOOL_TEXT):
            self.win.blit(self.preview_surf, (CANVAS_X, CANVAS_Y))

        if self.text_session:
            overlay = self.canvas.copy()
            self.text_session.render_preview(overlay)
            self.win.blit(overlay, (CANVAS_X, CANVAS_Y))

        pygame.draw.rect(self.win, UI_BORDER,
                         pygame.Rect(CANVAS_X, CANVAS_Y, CANVAS_W, CANVAS_H), 1)

        # ── Toolbar ──
        # ИЗМЕНЕНИЕ: Передаем events в тулбар
        rects = self._draw_toolbar(events)

        # === ВНИМАНИЕ: СТРОКИ С events_this_frame И pygame.event.post УДАЛЕНЫ ===

        # ── Notification ──
        now = pygame.time.get_ticks()
        if self._notif_text and now < self._notif_until:
            alpha = min(255, (self._notif_until - now) * 255 // 400)
            notif_surf = self.font_bold.render(self._notif_text, True,
                                               UI_ACCENT2)
            notif_surf.set_alpha(alpha)
            self.win.blit(notif_surf,
                          (CANVAS_X + 10, CANVAS_H - 30))

        # ── Cursor crosshair on canvas ──
        mx, my = pygame.mouse.get_pos()
        if self.on_canvas((mx, my)) and not self.text_session:
            sz = self.brush_px // 2 + 1
            pygame.draw.line(self.win, (100, 100, 100),
                             (mx - sz - 2, my), (mx + sz + 2, my), 1)
            pygame.draw.line(self.win, (100, 100, 100),
                             (mx, my - sz - 2), (mx, my + sz + 2), 1)

        pygame.display.flip()
        return rects

    def _draw_toolbar(self,events) -> dict:
        """Draw all toolbar elements; return dict of clickable rects."""
        rects = {"tools": {}, "sizes": {}, "palette": [], "clear": None, "save": None}
        surf  = self.win
        x0    = 0
        w     = TOOLBAR_W

        # panel bg
        pygame.draw.rect(surf, UI_PANEL, pygame.Rect(0, 0, w, WIN_H))
        pygame.draw.line(surf, UI_BORDER, (w - 1, 0), (w - 1, WIN_H), 1)

        y = 12

        # ── App title ──
        draw_text(surf, self.font_bold, "🎨  PAINT", UI_ACCENT, w // 2, y, "midtop")
        y += 28
        pygame.draw.line(surf, UI_BORDER, (10, y), (w - 10, y), 1)
        y += 8

        # ── Tools ──
        draw_text(surf, self.font_ui, "TOOLS", UI_TEXT_DIM, 12, y)
        y += 18

        btn_w = (w - 24) // 2
        btn_h = 34

        for row in TOOL_ROWS:
            for col_idx, tool in enumerate(row):
                if tool is None:
                    continue
                bx   = 8 + col_idx * (btn_w + 8)
                rect = pygame.Rect(bx, y, btn_w, btn_h)
                rects["tools"][tool] = rect

                is_sel = (self.active_tool == tool)
                bg     = UI_SEL  if is_sel  else (UI_HOVER if is_hovered(rect) else UI_PANEL)
                border = UI_ACCENT if is_sel else UI_BORDER

                pygame.draw.rect(surf, bg,     rect, border_radius=5)
                pygame.draw.rect(surf, border, rect, 1, border_radius=5)

                icon  = TOOL_ICONS.get(tool, "?")
                label = TOOL_LABELS.get(tool, tool)
                fg    = UI_ACCENT if is_sel else UI_TEXT
                draw_text(surf, self.font_icon, icon,  fg, bx + 10,       y + btn_h // 2, "midleft")
                draw_text(surf, self.font_ui,   label, fg, bx + btn_w - 6, y + btn_h // 2, "midright")

            y += btn_h + 4

        y += 4
        pygame.draw.line(surf, UI_BORDER, (10, y), (w - 10, y), 1)
        y += 8

        # ── Brush size ──
        draw_text(surf, self.font_ui, "BRUSH SIZE  (1 / 2 / 3)", UI_TEXT_DIM, 12, y)
        y += 18

        sz_labels = {1: "S  2px", 2: "M  5px", 3: "L  10px"}
        sz_w = (w - 24) // 3
        for i, (key, lbl) in enumerate(sz_labels.items()):
            bx   = 8 + i * (sz_w + 4)
            rect = pygame.Rect(bx, y, sz_w, 30)
            rects["sizes"][key] = rect
            is_sel = (self.brush_size_key == key)
            bg     = UI_SEL  if is_sel else (UI_HOVER if is_hovered(rect) else UI_PANEL)
            border = UI_ACCENT2 if is_sel else UI_BORDER
            pygame.draw.rect(surf, bg,     rect, border_radius=4)
            pygame.draw.rect(surf, border, rect, 1, border_radius=4)
            fg = UI_ACCENT2 if is_sel else UI_TEXT
            draw_text(surf, self.font_ui, lbl, fg, rect.centerx, rect.centery, "center")

        y += 38
        pygame.draw.line(surf, UI_BORDER, (10, y), (w - 10, y), 1)
        y += 8

        # ── Color swatches ──
        draw_text(surf, self.font_ui, "PALETTE  (L/R click)", UI_TEXT_DIM, 12, y)
        y += 18

        sw = 20
        gap = 2
        per_row = (w - 16) // (sw + gap)

        for i, col in enumerate(PALETTE):
            row_i = i // per_row
            col_i = i  % per_row
            bx    = 8 + col_i * (sw + gap)
            by    = y + row_i * (sw + gap)
            rect  = pygame.Rect(bx, by, sw, sw)
            rects["palette"].append(rect)
            pygame.draw.rect(surf, col,      rect, border_radius=3)
            # selection ring
            if col == self.color:
                pygame.draw.rect(surf, UI_ACCENT, rect, 2, border_radius=3)
            elif col == self.secondary_col:
                pygame.draw.rect(surf, (220, 80, 80), rect, 2, border_radius=3)

        palette_rows = math.ceil(len(PALETTE) / per_row)
        y += palette_rows * (sw + gap) + 6

        # ── Active colors preview ──
        draw_text(surf, self.font_ui, "PRIMARY / SECONDARY", UI_TEXT_DIM, 12, y)
        y += 18
        pygame.draw.rect(surf, self.secondary_col,
                         pygame.Rect(18, y + 8, 32, 32), border_radius=4)
        pygame.draw.rect(surf, UI_BORDER,
                         pygame.Rect(18, y + 8, 32, 32), 1, border_radius=4)
        pygame.draw.rect(surf, self.color,
                         pygame.Rect(8, y, 32, 32), border_radius=4)
        pygame.draw.rect(surf, UI_BORDER,
                         pygame.Rect(8, y, 32, 32), 1, border_radius=4)
        y += 50

        pygame.draw.line(surf, UI_BORDER, (10, y), (w - 10, y), 1)
        y += 8

        # ── Action buttons ──
        action_bw = w - 16
        clear_rect = pygame.Rect(8, y, action_bw, 30)
        rects["clear"] = clear_rect
        clr_bg = UI_HOVER if is_hovered(clear_rect) else UI_PANEL
        pygame.draw.rect(surf, clr_bg,    clear_rect, border_radius=5)
        pygame.draw.rect(surf, (200, 60, 60), clear_rect, 1, border_radius=5)
        draw_text(surf, self.font_ui, "Clear Canvas",
                  (220, 80, 80), clear_rect.centerx, clear_rect.centery, "center")
        y += 36

        save_rect = pygame.Rect(8, y, action_bw, 30)
        rects["save"] = save_rect
        sav_bg = UI_HOVER if is_hovered(save_rect) else UI_PANEL
        pygame.draw.rect(surf, sav_bg,   save_rect, border_radius=5)
        pygame.draw.rect(surf, UI_ACCENT2, save_rect, 1, border_radius=5)
        draw_text(surf, self.font_ui, "Save PNG  (Ctrl+S)",
                  UI_ACCENT2, save_rect.centerx, save_rect.centery, "center")
        y += 36

        # ── Status / hints ──
        pygame.draw.line(surf, UI_BORDER, (10, y), (w - 10, y), 1)
        y += 6
        hints = [
            f"Tool:  {TOOL_LABELS.get(self.active_tool, '')}",
            f"Size:  {self.brush_px}px",
        ]
        if self.text_session:
            hints += ["", "Typing — Enter=OK", "Escape=Cancel"]
        else:
            hints += ["", "Text: click canvas,", "then type + Enter"]

        for hint in hints:
            draw_text(surf, self.font_ui, hint, UI_TEXT_DIM, 10, y)
            y += 17

        # handle toolbar clicks here (inside the same frame)
        self._handle_toolbar_clicks(events, rects)

        return rects



if __name__ == "__main__":
    PaintApp().run()
