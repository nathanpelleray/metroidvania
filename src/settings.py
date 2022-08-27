from pathlib import Path

FPS = 60
TARGET_FPS = 60
DEBUG = True

TILE_SIZE = 64
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BASE_DIR = Path().resolve()

# colors 
BG_COLOR = '#060C17'
PLAYER_COLOR = '#C4F7FF'
TILE_COLOR = '#94D7F2'

# camera
CAMERA_BORDERS = {
    'left': 100,
    'right': 200,
    'top': 100,
    'bottom': 150
}
