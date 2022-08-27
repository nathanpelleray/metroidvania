import pygame

from src.settings import LAYERS


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], surf: pygame.Surface, groups: list[pygame.sprite.AbstractGroup],
                 z: int = LAYERS['main']):
        # Setup
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

    def draw_debug(self, display_surface: pygame.Surface, offset: pygame.math.Vector2):
        offset_rect = self.rect.copy()
        offset_rect.center -= offset
        pygame.draw.rect(display_surface, 'white', offset_rect, 3)


class AnimatedTile(Tile):
    def __init__(self, pos: tuple[int, int], frames: list[pygame.Surface],
                 groups: list[pygame.sprite.AbstractGroup], speed_animation: int = 5, z: int = LAYERS['main']):
        # Animation
        self.frames = frames
        self.frame_index = 0
        self.speed_animation = speed_animation

        # Setup
        super().__init__(
            pos=pos,
            surf=self.frames[self.frame_index],
            groups=groups,
            z=z
        )

    def animate(self, dt: float):
        self.frame_index += self.speed_animation * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt: float):
        self.animate(dt)
