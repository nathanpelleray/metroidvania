import pygame

from src.settings import TILE_SIZE, TILE_COLOR


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[pygame.sprite.AbstractGroup]):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(TILE_COLOR)
        self.rect = self.image.get_rect(topleft=pos)
