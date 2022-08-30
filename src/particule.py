import pygame

from src.settings import TARGET_FPS, BASE_DIR, LAYERS
from src.support import import_folder


class ParticuleManager:
    def __init__(self):
        self.frames = {
            'before_jump': import_folder(BASE_DIR / "graphics" / "particules" / "before_jump"),
            'after_jump': import_folder(BASE_DIR / "graphics" / "particules" / "after_jump"),
            'mushroom_death': import_folder(BASE_DIR / "graphics" / "enemies" / "mushroom" / "death"),
            'player_death': import_folder(BASE_DIR / "graphics" / "player" / "death")
        }

    def create_particules(self, animation_type: str, pos: tuple[int, int], group: pygame.sprite.Group):
        animation_frames = self.frames[animation_type]
        ParticuleEffect(pos, animation_frames, group)


class ParticuleEffect(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], animation_frames: list[pygame.Surface], group: pygame.sprite.Group):
        super().__init__(group)

        # Animation
        self.frames = animation_frames
        self.frame_index = 0
        self.animation_speed = 0.15 * TARGET_FPS

        # Setup
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['main']

    def animate(self, dt: float):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, dt: float):
        self.animate(dt)
