import pygame
from pytmx import load_pygame

from src.camera import CameraGroup
from src.player import Player
from src.settings import TILE_SIZE, BG_COLOR, BASE_DIR, DEBUG
from src.support import import_folder
from src.tile import Tile, AnimatedTile


class Level:
    def __init__(self):
        # Setup
        self.display_surface = pygame.display.get_surface()

        # Groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        # Player
        self.player = None

        self.setup()

    def setup(self):
        tmx_data = load_pygame('data/map_test.tmx')

        # Terrain
        for x, y, surf in tmx_data.get_layer_by_name('Terrain').tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

        # Water
        water_frames = import_folder(BASE_DIR / "graphics" / "water")
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            AnimatedTile((x * TILE_SIZE, y * TILE_SIZE), water_frames, [self.all_sprites])

        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)

    def run(self, dt: float):
        # Drawing logic
        self.display_surface.fill(BG_COLOR)
        self.all_sprites.draw(self.player)

        # Debug
        if DEBUG:
            self.all_sprites.draw_debug()

        # Update logic
        self.all_sprites.update(dt)
