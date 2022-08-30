import pygame
from pytmx import load_pygame

from src.UI import UI
from src.camera import CameraGroup
from src.enemy import Enemy
from src.player import Player
from src.settings import TILE_SIZE, BG_COLOR, BASE_DIR, DEBUG, LAYERS
from src.support import import_folder
from src.tile import Tile, AnimatedTile
from src.timer import Timer


class Level:
    def __init__(self):
        # Setup
        self.display_surface = pygame.display.get_surface()

        # Groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.collider_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Timers
        self.timers = {
            'screen shake': Timer(300, self.stop_screen_shake)
        }

        # Screen Shake
        self.screen_shake = False

        # Player
        self.player = None

        # Map
        self.setup()

        # User interface
        self.ui = UI()

    def setup(self):
        tmx_data = load_pygame('data/map_test.tmx')

        # Terrain
        for x, y, surf in tmx_data.get_layer_by_name('Terrain').tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), [self.all_sprites, self.collision_sprites], surf, LAYERS['terrain'])

        # Water
        water_frames = import_folder(BASE_DIR / "graphics" / "water")
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            AnimatedTile((x * TILE_SIZE, y * TILE_SIZE), water_frames, [self.all_sprites], z=LAYERS['water'], alpha=150)

        # Enemies
        for obj in tmx_data.get_layer_by_name('Enemies'):
            if obj.name == 'Collider':
                Tile((obj.x, obj.y), [self.collider_sprites], z=LAYERS['invisible'])
            if obj.type == 'Enemy':
                Enemy(obj.name, (obj.x, obj.y), [self.all_sprites, self.enemy_sprites], self.collider_sprites)

        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)

    def damage_player(self):
        if self.player.vulnerable:
            collision_sprites = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
            if collision_sprites:
                for _ in collision_sprites:
                    self.player.health -= 1
                    self.player.vulnerable = False
                    self.player.timers['invulnerability'].activate()
                    self.screen_shake = True
                    self.timers['screen shake'].activate()

    def stop_screen_shake(self):
        self.screen_shake = False

    def update_timers(self):
        for timer in self.timers.values():  # type: Timer
            timer.update()

    def run(self, dt: float):
        # Drawing logic
        self.display_surface.fill(BG_COLOR)
        self.all_sprites.custom_draw(self.player, self.screen_shake)
        self.ui.draw(self.player)

        # Debug
        if DEBUG:
            self.all_sprites.draw_debug()

        # Update logic
        self.all_sprites.update(dt)
        self.update_timers()
        self.damage_player()
