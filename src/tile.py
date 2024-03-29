import pygame

from src.settings import LAYERS, TILE_SIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int],
                 groups: list[pygame.sprite.AbstractGroup],
                 surf: pygame.Surface = pygame.Surface((TILE_SIZE, TILE_SIZE)),
                 z: int = LAYERS['main'],
                 alpha: int = 255):
        # Setup
        super().__init__(groups)
        self.image = surf
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

    def draw_debug(self, display_surface: pygame.Surface, offset: pygame.math.Vector2):
        offset_rect = self.rect.copy()
        offset_rect.center -= offset
        pygame.draw.rect(display_surface, 'white', offset_rect, 3)


class AnimatedTile(Tile):
    def __init__(self, pos: tuple[int, int], frames: list[pygame.Surface],
                 groups: list[pygame.sprite.AbstractGroup], speed_animation: int = 5, z: int = LAYERS['main'],
                 alpha: int = 255):
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
        self.alpha = alpha

    def animate(self, dt: float):
        self.frame_index += self.speed_animation * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.image.set_alpha(self.alpha)

    def update(self, dt: float):
        self.animate(dt)


class ExitTile(Tile):
    def __init__(self, current_level: str, new_level: str,
                 pos: tuple[int, int],
                 width: int, height: int,
                 groups: list[pygame.sprite.AbstractGroup],
                 ):
        # Setup
        super().__init__(
            pos=pos,
            groups=groups)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=pos)

        self.current_level = current_level
        self.new_level = new_level


class Checkpoint(Tile):
    def __init__(self, level_name: str,
                 pos: tuple[int, int],
                 groups: list[pygame.sprite.AbstractGroup],
                 ):
        # Setup
        super().__init__(
            pos=pos,
            groups=groups)
        self.level_name = level_name
