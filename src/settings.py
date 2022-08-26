from pathlib import Path

LEVEL_MAP = [
    '                            ',
    '                            ',
    '                            ',
    '       XXXX           XX    ',
    '   P                        ',
    'XXXXX         XX         XX ',
    ' XXXX       XX              ',
    ' XX    X  XXXX    XX  XX    ',
    '       X  XXXX    XX  XXX   ',
    '    XXXX  XXXXXX  XX  XXXX  ',
    'XXXXXXXX  XXXXXX  XX  XXXX  '
]

FPS = 60
TARGET_FPS = 60

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
