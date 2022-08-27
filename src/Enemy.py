from random import randint

import pygame

from src.settings import BASE_DIR, LAYERS, TARGET_FPS
from src.support import import_folder


class Enemy(pygame.sprite.Sprite):
    def __init__(self, monster_name: str, pos: tuple[int, int], groups: list[pygame.sprite.Group],
                 collider_sprites: pygame.sprite.Group):
        super().__init__(groups)

        # Animation
        self.animations = {
            'right_run': [], 'left_run': []
        }
        self.import_assets(monster_name)
        self.status = 'right_run'
        self.speed_animation = 6
        self.frame_index = 0

        # Setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['main']

        # Movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = randint(3, 5) * TARGET_FPS

        # Collision
        self.collider_sprites = collider_sprites

    def import_assets(self, name: str):
        path = BASE_DIR / "graphics" / "enemies" / name

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(path / animation)

    def animate(self, dt: float):
        self.frame_index += self.speed_animation * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def get_status(self):
        if self.speed > 0:
            self.status = 'right_run'
        else:
            self.status = 'left_run'

    def collision(self):
        if pygame.sprite.spritecollide(self, self.collider_sprites, False):
            self.speed *= -1

    def move(self, dt: float):
        self.pos.x += self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision()

    def update(self, dt: float):
        self.get_status()

        self.move(dt)
        self.animate(dt)
