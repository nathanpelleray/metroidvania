import pygame

from src.player import Player
from src.settings import LEVEL_MAP, TILE_SIZE, BG_COLOR, CAMERA_BORDERS
from src.tile import Tile


class Level:
    def __init__(self):
        # Setup
        self.display_surface = pygame.display.get_surface()

        # Groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        # Player
        self.player = None

        self.setup_level()

    def setup_level(self):
        for row_index, row in enumerate(LEVEL_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'X':
                    Tile((x, y), [self.all_sprites, self.collision_sprites])
                if col == 'P':
                    self.player = Player((x, y), self.all_sprites, self.collision_sprites)

    def run(self, dt: float):
        # Drawing logic
        self.display_surface.fill(BG_COLOR)
        self.all_sprites.draw(self.player)

        # Update logic
        self.all_sprites.update(dt)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100, 300)

        # camera
        cam_left = CAMERA_BORDERS['left']
        cam_top = CAMERA_BORDERS['top']
        cam_width = self.display_surface.get_size()[0] - (cam_left + CAMERA_BORDERS['right'])
        cam_height = self.display_surface.get_size()[1] - (cam_top + CAMERA_BORDERS['bottom'])

        self.camera_rect = pygame.Rect(cam_left, cam_top, cam_width, cam_height)

    def draw(self, player: Player):
        # getting the camera position
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        # camera offset
        self.offset = pygame.math.Vector2(
            self.camera_rect.left - CAMERA_BORDERS['left'],
            self.camera_rect.top - CAMERA_BORDERS['top'])

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
