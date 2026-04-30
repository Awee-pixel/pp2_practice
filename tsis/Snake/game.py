import pygame
import random
import math
from config import *

class Food:
    def __init__(self, ftype: str, pos: tuple[int, int], now_ms: int):
        self.type    = ftype
        self.pos     = pos          # (col, row)
        self.born_ms = now_ms
        self.color   = FOOD_COLORS[ftype]
        self.points  = FOOD_POINTS[ftype]
        self.lifetime = FOOD_LIFETIME[ftype]   # None = immortal

    def is_expired(self, now_ms: int) -> bool:
        if self.lifetime is None:
            return False
        return now_ms - self.born_ms >= self.lifetime

    def draw(self, surface: pygame.Surface, grid_offset_y: int):
        x = self.pos[0] * CELL_SIZE
        y = self.pos[1] * CELL_SIZE + grid_offset_y
        r = CELL_SIZE // 2 - 2
        cx, cy = x + CELL_SIZE // 2, y + CELL_SIZE // 2

        # pulsing alpha overlay
        progress = ((pygame.time.get_ticks() % 900) / 900)
        pulse    = int(abs(math.sin(progress * math.pi)) * 80)

        pygame.draw.circle(surface, self.color, (cx, cy), r)
        if self.type == FOOD_POISON:
            # skull-like X mark
            pygame.draw.line(surface, WHITE, (cx-4, cy-4), (cx+4, cy+4), 2)
            pygame.draw.line(surface, WHITE, (cx+4, cy-4), (cx-4, cy+4), 2)
        elif self.type == FOOD_BONUS:
            pygame.draw.circle(surface, WHITE, (cx, cy), r // 2)

        # countdown ring for timed foods
        if self.lifetime:
            remaining = max(0, self.lifetime - (pygame.time.get_ticks() - self.born_ms))
            frac      = remaining / self.lifetime
            if frac < 0.4:
                warn_color = (255, 80, 80, 180)
                pygame.draw.circle(surface, (255, 80, 80), (cx, cy), r + 2, 1)


class PowerUp:
    def __init__(self, pu_type: str, pos: tuple[int, int], now_ms: int):
        self.type    = pu_type
        self.pos     = pos
        self.born_ms = now_ms
        self.color   = PU_COLORS[pu_type]
        self.label   = PU_LABELS[pu_type]

    def is_expired(self, now_ms: int) -> bool:
        return now_ms - self.born_ms >= PU_FIELD_TIME

    def draw(self, surface: pygame.Surface, grid_offset_y: int,
             font: pygame.font.Font):
        x  = self.pos[0] * CELL_SIZE
        y  = self.pos[1] * CELL_SIZE + grid_offset_y
        cx = x + CELL_SIZE // 2
        cy = y + CELL_SIZE // 2
        r  = CELL_SIZE // 2 - 1

        # rotating border
        angle   = (pygame.time.get_ticks() // 4) % 360
        col_dim = tuple(max(0, c - 80) for c in self.color)
        pygame.draw.circle(surface, col_dim, (cx, cy), r + 3)
        pygame.draw.circle(surface, self.color, (cx, cy), r)

        # 1-letter label
        lbl = font.render(self.label[0], True, BLACK)
        surface.blit(lbl, lbl.get_rect(center=(cx, cy)))

        # time-left bar (thin strip under cell)
        remaining = max(0, PU_FIELD_TIME - (pygame.time.get_ticks() - self.born_ms))
        frac      = remaining / PU_FIELD_TIME
        bar_w     = int(CELL_SIZE * frac)
        bar_rect  = pygame.Rect(x, y + CELL_SIZE - 3, bar_w, 3)
        pygame.draw.rect(surface, self.color, bar_rect)

class Snake:
    def __init__(self, color: list):
        self.color  = tuple(color)
        self.reset()

    def reset(self):
        cx = COLS // 2
        cy = ROWS // 2
        self.body      = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.next_dir  = (1, 0)
        self.grow      = 0

    def set_direction(self, d: tuple[int, int]):
        # Prevent 180-degree reversal
        if (d[0] != -self.direction[0]) or (d[1] != -self.direction[1]):
            self.next_dir = d

    def move(self) -> tuple[int, int]:
        self.direction = self.next_dir
        head  = self.body[0]
        new_h = (head[0] + self.direction[0],
                 head[1] + self.direction[1])
        self.body.insert(0, new_h)
        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop()
        return new_h

    def grow_by(self, n: int):
        self.grow += n

    def shorten(self, n: int) -> bool:
        for _ in range(n):
            if len(self.body) > 1:
                self.body.pop()
        return len(self.body) > 1

    def head(self) -> tuple[int, int]:
        return self.body[0]

    def check_self_collision(self) -> bool:
        return self.body[0] in self.body[1:]

    def draw(self, surface: pygame.Surface, grid_offset_y: int):
        for i, (col, row) in enumerate(self.body):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + grid_offset_y
            rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
            shade = max(40, 255 - i * 6)
            seg_color = tuple(min(255, int(c * shade / 255))
                              for c in self.color)
            pygame.draw.rect(surface, seg_color, rect, border_radius=4)
            if i == 0:  # head highlight
                eye_off = (CELL_SIZE // 4, CELL_SIZE // 4)
                pygame.draw.circle(surface, WHITE,
                    (x + eye_off[0] + CELL_SIZE // 2,
                     y + eye_off[1]), 2)


class GameState:
    def __init__(self, snake_color, personal_best: int = 0):
        self.snake         = Snake(snake_color)
        self.personal_best = personal_best

        self.score         = 0
        self.level         = 1
        self.food_eaten    = 0     # within current level

        self.foods: list[Food]    = []
        self.powerup: PowerUp | None  = None
        self.obstacles: set[tuple]    = set()

        # active power-up effects
        self.active_pu: str | None = None
        self.pu_end_ms: int        = 0

        # shield status
        self.shield_active = False

        # speed
        self.base_move_interval = 1000 // BASE_SPEED   # ms between moves
        self._move_timer = 0

        # food spawn timer
        self._pu_spawn_timer = 0

        self._spawn_food(FOOD_NORMAL)
        self._maybe_spawn_bonus_food()

    def move_interval(self) -> int:
        lvl_bonus = (self.level - 1) * SPEED_INC
        base      = max(60, 1000 // (BASE_SPEED + lvl_bonus))
        if self.active_pu == PU_SPEED:
            return max(60, base - (1000 // SPEED_BOOST))
        if self.active_pu == PU_SLOW:
            slowdown = max(0, abs(SPEED_SLOW))
            return min(400, base + slowdown * 25)
        return base

    def _occupied(self) -> set[tuple]:
        """All cells that must not be used for spawning."""
        occupied = set(self.snake.body) | self.obstacles
        for f in self.foods:
            occupied.add(f.pos)
        if self.powerup:
            occupied.add(self.powerup.pos)
        return occupied

    def _random_free_cell(self) -> tuple[int, int] | None:
        occupied = self._occupied()
        free = [(c, r) for c in range(COLS) for r in range(ROWS)
                if (c, r) not in occupied]
        return random.choice(free) if free else None

    def _spawn_food(self, ftype: str):
        pos = self._random_free_cell()
        if pos:
            self.foods.append(Food(ftype, pos, pygame.time.get_ticks()))

    def _maybe_spawn_bonus_food(self):
        if not any(f.type == FOOD_BONUS for f in self.foods):
            if random.random() < 0.4:
                self._spawn_food(FOOD_BONUS)

    def _maybe_spawn_poison(self):
        if not any(f.type == FOOD_POISON for f in self.foods):
            if random.random() < 0.3:
                self._spawn_food(FOOD_POISON)

    def _spawn_powerup(self):
        if self.powerup is not None:
            return
        if random.random() < 0.25:
            pu_type = random.choice([PU_SPEED, PU_SLOW, PU_SHIELD])
            pos     = self._random_free_cell()
            if pos:
                self.powerup = PowerUp(pu_type, pos, pygame.time.get_ticks())

    def _place_obstacles(self):
        """Place obstacle blocks for the current level (level >= 3)."""
        n_blocks = (self.level - OBSTACLE_START_LEVEL + 1) * OBSTACLES_PER_LEVEL
        head     = self.snake.head()
        safe = {(head[0] + dx, head[1] + dy)
                for dx in range(-5, 6) for dy in range(-5, 6)}
        safe |= set(self.snake.body)

        attempts = 0
        while len(self.obstacles) < n_blocks and attempts < 1000:
            attempts += 1
            c = random.randint(0, COLS - 1)
            r = random.randint(0, ROWS - 1)
            if (c, r) not in safe and (c, r) not in self.obstacles:
                self.obstacles.add((c, r))
                # make sure food / powerup still have room
                if not self._random_free_cell():
                    self.obstacles.discard((c, r))

    def update(self, dt_ms: int) -> str:
        """
        Advance game logic by dt_ms milliseconds.
        Returns:
          "alive"    — normal tick
          "gameover" — collision / length 0
        """
        now = pygame.time.get_ticks()

        # expire power-up effect
        if self.active_pu and now >= self.pu_end_ms:
            self.active_pu = None

        # expire field power-up item
        if self.powerup and self.powerup.is_expired(now):
            self.powerup = None

        # expire timed foods
        self.foods = [f for f in self.foods if not f.is_expired(now)]
        if not any(f.type == FOOD_NORMAL for f in self.foods):
            self._spawn_food(FOOD_NORMAL)

        # move timer
        self._move_timer += dt_ms
        if self._move_timer < self.move_interval():
            return "alive"
        self._move_timer = 0

        # ── move snake ──
        new_head = self.snake.move()

        # wall collision
        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            if self.shield_active:
                self.shield_active = False
                # wrap-around (shield absorbs it)
                new_head = (new_head[0] % COLS, new_head[1] % ROWS)
                self.snake.body[0] = new_head
            else:
                return "gameover"

        # obstacle collision
        if new_head in self.obstacles:
            if self.shield_active:
                self.shield_active = False
            else:
                return "gameover"

        # self collision
        if self.snake.check_self_collision():
            if self.shield_active:
                self.shield_active = False
            else:
                return "gameover"

        # ── food collision ──
        for food in self.foods[:]:
            if new_head == food.pos:
                self.foods.remove(food)
                if food.type == FOOD_POISON:
                    alive = self.snake.shorten(2)
                    if not alive:
                        return "gameover"
                else:
                    self.score     += food.points
                    self.food_eaten += 1
                    self.snake.grow_by(1)
                    # level up?
                    if self.food_eaten >= FOOD_PER_LEVEL:
                        self.food_eaten = 0
                        self.level     += 1
                        if self.level >= OBSTACLE_START_LEVEL:
                            self._place_obstacles()
                self._spawn_food(FOOD_NORMAL)
                self._maybe_spawn_bonus_food()
                self._maybe_spawn_poison()
                break

        if self.powerup and new_head == self.powerup.pos:
            pu = self.powerup
            self.powerup = None
            if pu.type == PU_SHIELD:
                self.shield_active = True
            else:
                self.active_pu = pu.type
                self.pu_end_ms = now + PU_DURATION
        self._pu_spawn_timer += dt_ms
        if self._pu_spawn_timer >= 8000:
            self._pu_spawn_timer = 0
            self._spawn_powerup()

        return "alive"

    def draw(self, surface: pygame.Surface, grid_offset_y: int,
             show_grid: bool, small_font: pygame.font.Font):

        # grid overlay
        if show_grid:
            for c in range(COLS + 1):
                x = c * CELL_SIZE
                pygame.draw.line(surface, (30, 30, 50),
                                 (x, grid_offset_y),
                                 (x, grid_offset_y + ROWS * CELL_SIZE))
            for r in range(ROWS + 1):
                y = r * CELL_SIZE + grid_offset_y
                pygame.draw.line(surface, (30, 30, 50),
                                 (0, y), (COLS * CELL_SIZE, y))

        # obstacles
        for (c, r) in self.obstacles:
            x = c * CELL_SIZE
            y = r * CELL_SIZE + grid_offset_y
            pygame.draw.rect(surface, (80, 80, 100),
                             pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, (50, 50, 70),
                             pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), 1)

        # foods
        for food in self.foods:
            food.draw(surface, grid_offset_y)

        # power-up
        if self.powerup:
            self.powerup.draw(surface, grid_offset_y, small_font)

        # snake
        self.snake.draw(surface, grid_offset_y)
