from pathlib import Path

# Utils
FPS = 10000
TARGET_FPS = 60
DEBUG = False

# Screen
TILE_SIZE = 64
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FULLSCREEN = False

# Path file
BASE_DIR = Path().resolve()

# Colors
BG_COLOR = '#060C17'
PLAYER_COLOR = '#C4F7FF'
TILE_COLOR = '#94D7F2'

# Camera
CAMERA_BORDERS = {
    'left': SCREEN_WIDTH // 2 - 50,
    'right': SCREEN_WIDTH // 2 + 50,
    'top': SCREEN_HEIGHT // 2 - 50,
    'bottom': SCREEN_HEIGHT // 2 + 50
}

# Layer
LAYERS = {
    'invisible': 0,
    'water background': 1,
    'terrain': 2,
    'main': 3,
    'water': 4,
}
