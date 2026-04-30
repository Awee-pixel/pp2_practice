import pygame
import math
from collections import deque



BRUSH_SIZES = {1: 2, 2: 5, 3: 10}   # key → px width

TOOL_PENCIL   = "pencil"
TOOL_LINE     = "line"
TOOL_RECT     = "rect"
TOOL_CIRCLE   = "circle"
TOOL_SQUARE   = "square"
TOOL_RTRI     = "right_tri"
TOOL_ETRI     = "equil_tri"
TOOL_RHOMBUS  = "rhombus"
TOOL_FILL     = "fill"
TOOL_ERASER   = "eraser"
TOOL_TEXT     = "text"


def flood_fill(surface: pygame.Surface, x: int, y: int,
               fill_color: tuple, tolerance: int = 0):
    """
    Iterative 4-connected flood fill.
    Fills all pixels matching the color at (x, y) with fill_color.
    tolerance=0 → exact match.
    """
    w, h = surface.get_size()
    if not (0 <= x < w and 0 <= y < h):
        return

    target_color = surface.get_at((x, y))[:3]
    fill_rgb     = fill_color[:3]

    if target_color == fill_rgb:
        return          # already that color — nothing to do

    # Lock once for performance
    surface.lock()
    try:
        visited = set()
        queue   = deque()
        queue.append((x, y))

        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) in visited:
                continue
            if not (0 <= cx < w and 0 <= cy < h):
                continue
            pixel = surface.get_at((cx, cy))[:3]
            if pixel != target_color:
                continue
            visited.add((cx, cy))
            surface.set_at((cx, cy), fill_rgb)
            queue.append((cx + 1, cy))
            queue.append((cx - 1, cy))
            queue.append((cx, cy + 1))
            queue.append((cx, cy - 1))
    finally:
        surface.unlock()

def draw_rect(surface, color, x1, y1, x2, y2, width):
    x, y   = min(x1, x2), min(y1, y2)
    w, h   = abs(x2 - x1), abs(y2 - y1)
    if w == 0 or h == 0:
        return
    pygame.draw.rect(surface, color, pygame.Rect(x, y, w, h), width)


def draw_circle(surface, color, x1, y1, x2, y2, width):
    cx   = (x1 + x2) // 2
    cy   = (y1 + y2) // 2
    rx   = abs(x2 - x1) // 2
    ry   = abs(y2 - y1) // 2
    r    = max(rx, ry)
    if r == 0:
        return
    pygame.draw.circle(surface, color, (cx, cy), r, width)


def draw_square(surface, color, x1, y1, x2, y2, width):
    side = max(abs(x2 - x1), abs(y2 - y1))
    sx   = x1 if x2 >= x1 else x1 - side
    sy   = y1 if y2 >= y1 else y1 - side
    pygame.draw.rect(surface, color, pygame.Rect(sx, sy, side, side), width)


def draw_right_triangle(surface, color, x1, y1, x2, y2, width):
    # right angle at (x1, y2)
    pts = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, pts, width)


def draw_equil_triangle(surface, color, x1, y1, x2, y2, width):
    # base from (x1,y2) to (x2,y2), apex midpoint above
    mid_x  = (x1 + x2) / 2
    height = abs(x2 - x1) * math.sqrt(3) / 2
    top_y  = y2 - height if y1 <= y2 else y2 + height
    pts    = [(x1, y2), (x2, y2), (mid_x, top_y)]
    pygame.draw.polygon(surface, color, pts, width)


def draw_rhombus(surface, color, x1, y1, x2, y2, width):
    cx   = (x1 + x2) // 2
    cy   = (y1 + y2) // 2
    pts  = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
    pygame.draw.polygon(surface, color, pts, width)


def draw_straight_line(surface, color, x1, y1, x2, y2, width):
    pygame.draw.line(surface, color, (x1, y1), (x2, y2), max(1, width))


SHAPE_DRAWERS = {
    TOOL_LINE:    draw_straight_line,
    TOOL_RECT:    draw_rect,
    TOOL_CIRCLE:  draw_circle,
    TOOL_SQUARE:  draw_square,
    TOOL_RTRI:    draw_right_triangle,
    TOOL_ETRI:    draw_equil_triangle,
    TOOL_RHOMBUS: draw_rhombus,
}


def draw_shape(tool, surface, color, x1, y1, x2, y2, width):
    fn = SHAPE_DRAWERS.get(tool)
    if fn:
        fn(surface, color, x1, y1, x2, y2, width)

class TextSession:
    def __init__(self, x: int, y: int, color: tuple,
                 font: pygame.font.Font):
        self.x      = x
        self.y      = y
        self.color  = color
        self.font   = font
        self.buffer = ""
        self.active = True

    def feed_event(self, event: pygame.event.Event) -> str:
        """
        Feed a KEYDOWN event.
        Returns:
          "confirm" — Enter pressed, commit text
          "cancel"  — Escape pressed
          "typing"  — still editing
        """
        if event.type != pygame.KEYDOWN:
            return "typing"
        if event.key == pygame.K_RETURN:
            return "confirm"
        if event.key == pygame.K_ESCAPE:
            return "cancel"
        if event.key == pygame.K_BACKSPACE:
            self.buffer = self.buffer[:-1]
        elif event.unicode and event.unicode.isprintable():
            self.buffer += event.unicode
        return "typing"

    def render_preview(self, surface: pygame.Surface):
        """Draw the current buffer with a blinking cursor onto surface."""
        display = self.buffer + ("|" if (pygame.time.get_ticks() // 530) % 2 == 0
                                 else " ")
        rendered = self.font.render(display, True, self.color)
        # semi-transparent background for readability
        bg = pygame.Surface(
            (rendered.get_width() + 4, rendered.get_height() + 2),
            pygame.SRCALPHA)
        bg.fill((255, 255, 255, 120))
        surface.blit(bg, (self.x - 2, self.y - 1))
        surface.blit(rendered, (self.x, self.y))

    def commit(self, surface: pygame.Surface):
        """Blit the final text permanently onto surface."""
        if self.buffer.strip():
            rendered = self.font.render(self.buffer, True, self.color)
            surface.blit(rendered, (self.x, self.y))
