import pygame

from src.player import Player
from src.settings import BASE_DIR, LAYERS
from src.support import import_folder


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player: Player, direction: str, groups: list[pygame.sprite.Group], z: int = LAYERS['main']):
        super().__init__(groups)
        direction_player = player.status.split('_')[0]

        # Animation
        full_path = BASE_DIR / "graphics" / "player" / f"{direction}_sword_effect"
        self.frames = import_folder(full_path)
        self.speed_animation = 4 * 3
        self.frame_index = 0

        # Setup
        self.image = self.frames[self.frame_index]
        self.z = z
        if direction == 'right':
            self.rect = self.image.get_rect(topleft=player.rect.topright)
        elif direction == 'bottom':
            self.rect = self.image.get_rect(topleft=player.rect.bottomleft)
        elif direction == 'top':
            self.rect = self.image.get_rect(bottomleft=player.rect.topleft)
        else:
            self.rect = self.image.get_rect(topright=player.rect.topleft)

    def animate(self, dt: float):
        self.frame_index += self.speed_animation * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def draw_debug(self, display_surface: pygame.Surface, offset: pygame.math.Vector2):
        # draw rect
        offset_rect = self.rect.copy()
        offset_rect.topleft -= offset
        pygame.draw.rect(display_surface, 'white', offset_rect, 3)

    def update(self, dt: float):
        self.animate(dt)
