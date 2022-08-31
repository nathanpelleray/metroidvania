from random import randint

import pygame

from src.player import Player
from src.settings import CAMERA_BORDERS, LAYERS
from src.tile import Tile


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

    def custom_draw(self, player: Player, screen_shake: bool):
        # getting the camera position
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        # Camera offset
        self.offset = pygame.math.Vector2(
            self.camera_rect.left - CAMERA_BORDERS['left'],
            self.camera_rect.top - CAMERA_BORDERS['top']
        )

        # Screen shake
        offset_screen_shake = pygame.math.Vector2()
        if screen_shake:
            offset_screen_shake.x = randint(-4, 4)
            offset_screen_shake.y = randint(-4, 4)

        # Draw sprites
        for layer in LAYERS.values():
            for sprite in self.sprites():  # type: Tile
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft - self.offset + offset_screen_shake
                    self.display_surface.blit(sprite.image, offset_pos)

    def draw_debug(self):
        # camera offset
        self.offset = pygame.math.Vector2(
            self.camera_rect.left - CAMERA_BORDERS['left'],
            self.camera_rect.top - CAMERA_BORDERS['top']
        )

        for sprite in self.sprites():
            if hasattr(sprite, 'draw_debug'):
                sprite.draw_debug(self.display_surface, self.offset)

    def empty(self):
        for sprite in self.sprites():
            if not hasattr(sprite, 'input'):
                sprite.kill()
