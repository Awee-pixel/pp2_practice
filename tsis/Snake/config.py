# Window
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 640
TITLE         = "Snake Game"
FPS           = 60

# Grid
CELL_SIZE  = 20
COLS       = WINDOW_WIDTH  // CELL_SIZE   # 40
ROWS       = (WINDOW_HEIGHT - 80) // CELL_SIZE  # 28  (80 px HUD)
HUD_HEIGHT = 80

# Colors
BLACK       = (0,   0,   0)
WHITE       = (255, 255, 255)
DARK_BG     = (15,  15,  25)
PANEL_BG    = (25,  25,  40)
ACCENT      = (0,   220, 120)
ACCENT2     = (0,   170, 255)
RED         = (220, 50,  50)
YELLOW      = (255, 210, 0)
ORANGE      = (255, 140, 0)
PURPLE      = (160, 0,   220)
GRAY        = (100, 100, 120)
LIGHT_GRAY  = (180, 180, 200)
DARK_RED    = (140, 20,  20)
GOLD        = (255, 200, 50)

# Food types
FOOD_NORMAL  = "normal"
FOOD_BONUS   = "bonus"
FOOD_POISON  = "poison"

FOOD_COLORS = {
    FOOD_NORMAL: (80,  200, 80),
    FOOD_BONUS:  (255, 180, 0),
    FOOD_POISON: DARK_RED,
}
FOOD_POINTS = {
    FOOD_NORMAL: 10,
    FOOD_BONUS:  30,
    FOOD_POISON: 0,
}
FOOD_LIFETIME = {
    FOOD_NORMAL: None,   # never expires
    FOOD_BONUS:  7000,   # ms
    FOOD_POISON: 10000,  # ms
}

# Power-up types
PU_SPEED  = "speed_boost"
PU_SLOW   = "slow_motion"
PU_SHIELD = "shield"

PU_COLORS = {
    PU_SPEED:  (0,   220, 255),
    PU_SLOW:   (180, 0,   255),
    PU_SHIELD: (255, 215, 0),
}
PU_LABELS = {
    PU_SPEED:  "SPEED",
    PU_SLOW:   "SLOW",
    PU_SHIELD: "SHIELD",
}
PU_DURATION    = 5000   # ms — active effect lasts 5 s
PU_FIELD_TIME  = 8000   # ms — disappears from field after 8 s

# Speed settings
BASE_SPEED   = 8    # moves/sec
SPEED_INC    = 1    # per level
SPEED_BOOST  = 5
SPEED_SLOW   = -4

# Level progression
FOOD_PER_LEVEL = 5

# Obstacle settings (from level 3)
OBSTACLE_START_LEVEL = 3
OBSTACLES_PER_LEVEL  = 4   # extra blocks each new level

# Default settings (overridden by settings.json)
DEFAULT_SETTINGS = {
    "snake_color": [0, 200, 100],
    "grid_overlay": False,
    "sound": False,
}
