import pygame

from src.particule import ParticuleManager
from src.settings import TARGET_FPS, BASE_DIR, LAYERS
from src.support import import_folder, wave_value
from src.tile import Tile
from src.timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], group: pygame.sprite.Group,
                 collision_sprites: pygame.sprite.Group):
        super().__init__(group)

        # Animation
        self.animations = {
            'right_idle': [], 'left_idle': [],
            'right_run': [], 'left_run': [],
            'right_jump': [], 'left_jump': [],
            'right_fall': [], 'left_fall': []
        }
        self.import_assets()
        self.status = 'right_idle'
        self.speed_animation = 4
        self.frame_index = 0

        # Setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['main']

        # Movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 8 * TARGET_FPS
        self.gravity = 0.8 * TARGET_FPS
        self.jump_speed = 20
        self.collision_sprites = collision_sprites
        self.on_floor = False
        self.can_double_jump = False
        self.can_dash = True

        # Stats
        self.max_health = 3
        self.health = self.max_health

        # Interaction
        self.vulnerable = True

        # Timer
        self.timers = {
            'double jump': Timer(500, self.activate_double_jump),
            'dash': Timer(100, self.stop_dash),
            'reset dash': Timer(500, self.reset_dash),
            'invulnerability': Timer(500, self.reset_vulnerability)
        }

        # Player particule
        self.particule_manager = ParticuleManager()

    def import_assets(self):
        for animation in self.animations.keys():
            full_path = BASE_DIR / "graphics" / "player" / animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt: float):
        self.frame_index += self.speed_animation * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

        # hit
        if not self.vulnerable and not self.timers['dash'].active:
            alpha = wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['dash'].active:
            # Movement
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # Jump
            if keys[pygame.K_SPACE] and (self.on_floor or self.can_double_jump):
                if self.on_floor:
                    self.timers['double jump'].activate()
                self.can_double_jump = False
                self.direction.y = -self.jump_speed
                self.frame_index = 0
                self.particule_manager.create_particules('before_jump', self.rect.topleft, [self.groups()[0]])

            # Dash
            if keys[pygame.K_RCTRL] and self.can_dash:
                self.direction.y = 0
                self.can_dash = False
                self.timers['dash'].activate()
                self.vulnerable = False
                self.speed *= 4

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        if self.direction.y < 0:
            self.status = self.status.split('_')[0] + '_jump'
        elif self.direction.y > 1:
            self.status = self.status.split('_')[0] + '_fall'
        else:
            if self.direction.x != 0:
                self.status = self.status.split('_')[0] + '_run'

    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                self.pos.x = self.rect.x

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():  # type: Tile
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_floor = True
                    self.can_double_jump = False
                    if 'fall' in self.status:
                        self.particule_manager.create_particules('after_jump', self.rect.topleft, [self.groups()[0]])
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
                self.pos.y = self.rect.y

        if self.on_floor and self.direction.y != 0:
            self.on_floor = False

    def apply_gravity(self, dt: float):
        self.direction.y += self.gravity * dt
        self.pos.y += self.direction.y * dt * TARGET_FPS
        self.rect.y = round(self.pos.y)

    def move(self, dt: float):
        # Horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.horizontal_collisions()

        # Vertical
        self.apply_gravity(dt)
        self.vertical_collisions()

    def draw_debug(self, display_surface: pygame.Surface, offset: pygame.math.Vector2):
        # draw rect
        offset_rect = self.rect.copy()
        offset_rect.topleft -= offset
        pygame.draw.rect(display_surface, 'white', offset_rect, 3)

    def activate_double_jump(self):
        self.can_double_jump = True

    def stop_dash(self):
        self.speed = 8 * TARGET_FPS
        self.timers['reset dash'].activate()
        self.vulnerable = True

    def reset_dash(self):
        self.can_dash = True

    def reset_vulnerability(self):
        self.vulnerable = True

    def update_timers(self):
        for timer in self.timers.values():  # type: Timer
            timer.update()

    def update(self, dt: float):
        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)
