import pygame

from src.settings import TILE_SIZE, TILE_COLOR


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], surf: pygame.Surface, groups: list[pygame.sprite.AbstractGroup]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
