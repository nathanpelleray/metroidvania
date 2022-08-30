from random import randint

import pygame

from src.particule import ParticuleManager
from src.player import Player
from src.settings import BASE_DIR, LAYERS, TARGET_FPS
from src.support import import_folder, wave_value
from src.timer import Timer


class Enemy(pygame.sprite.Sprite):
    def __init__(self, monster_name: str, pos: tuple[int, int], groups: list[pygame.sprite.Group],
                 collider_sprites: pygame.sprite.Group):
        super().__init__(groups)
        self.monster_name = monster_name

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

        # Timers
        self.timers = {
            'invulnerability': Timer(350, self.reset_vulnerability)
        }

        # Stats
        self.health = 50
        self.vulnerable = True

        # Collision
        self.collider_sprites = collider_sprites

        # Player particule
        self.particule_manager = ParticuleManager()

    def import_assets(self, name: str):
        path = BASE_DIR / "graphics" / "enemies" / name

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(path / animation)

    def animate(self, dt: float):
        self.frame_index += self.speed_animation * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

        # hit
        if not self.vulnerable:
            alpha = wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_status(self):
        if self.speed > 0:
            self.status = 'right_run'
        else:
            self.status = 'left_run'

    def collision(self):
        if pygame.sprite.spritecollide(self, self.collider_sprites, False):
            self.speed *= -1

    def move(self, dt: float):
        if self.vulnerable:
            self.pos.x += self.speed * dt
            self.rect.x = round(self.pos.x)
            self.collision()

    def get_damage(self, player: Player):
        if self.vulnerable:
            self.health -= player.damage
            self.vulnerable = False
            self.timers['invulnerability'].activate()

    def check_death(self):
        if self.health <= 0:
            self.particule_manager.create_particules(f'{self.monster_name}_death', self.rect.topleft,
                                                     [self.groups()[0]])
            self.kill()

    def draw_debug(self, display_surface: pygame.Surface, offset: pygame.math.Vector2):
        # draw rect
        offset_rect = self.rect.copy()
        offset_rect.topleft -= offset
        pygame.draw.rect(display_surface, 'white', offset_rect, 3)

    def reset_vulnerability(self):
        self.vulnerable = True

    def update_timers(self):
        for timer in self.timers.values():  # type: Timer
            timer.update()

    def update(self, dt: float):
        self.get_status()
        self.update_timers()
        self.check_death()

        self.move(dt)
        self.animate(dt)
