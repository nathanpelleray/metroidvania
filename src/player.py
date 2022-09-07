import pygame

from src.settings import TARGET_FPS, BASE_DIR, LAYERS
from src.support import import_folder, wave_value
from src.tile import Tile
from src.timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], group: pygame.sprite.Group,
                 collision_sprites: pygame.sprite.Group, create_attack, destroy_attack, create_particules,
                 joysticks: list[pygame.joystick.Joystick]):
        super().__init__(group)

        # Animation
        self.animations = {
            'right_idle': [], 'left_idle': [],
            'right_run': [], 'left_run': [],
            'right_jump': [], 'left_jump': [],
            'right_fall': [], 'left_fall': [],
            'right_attack': [], 'left_attack': []
        }
        self.import_assets()
        self.status = 'right_idle'
        self.speed_animation = 4
        self.frame_index = 0
        self.alpha = 255

        # Setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['main']
        self.joysticks = joysticks

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
        self.can_attack = True

        # Stats
        self.max_health = 3
        self.health = self.max_health
        self.damage = 10

        # Interaction
        self.vulnerable = True
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        # Timer
        self.timers = {
            'double jump': Timer(500, self.activate_double_jump),
            'dash': Timer(100, self.stop_dash),
            'reset dash': Timer(500, self.reset_dash),
            'invulnerability': Timer(500, self.reset_vulnerability),
            'attacking': Timer(300, self.stop_attack),
            'reset attack': Timer(500, self.reset_attack)
        }

        # Player particule
        self.create_particules = create_particules

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
            self.image.set_alpha(self.alpha)

    def change_joysticks(self, joysticks: list[pygame.joystick.Joystick]):
        self.joysticks = joysticks

    def input(self):
        if not self.timers['dash'].active and not self.timers['attacking'].active:
            if len(self.joysticks) == 0:
                keys = pygame.key.get_pressed()

                # Movement
                if keys[pygame.K_RIGHT]:
                    self.direction.x = 1
                    self.status = 'right'
                elif keys[pygame.K_LEFT]:
                    self.direction.x = -1
                    self.status = 'left'
                else:
                    self.direction.x = 0

                # Attack
                if keys[pygame.K_q] and self.can_attack:
                    self.timers['attacking'].activate()
                    self.speed_animation = 4 * 3
                    self.frame_index = 0
                    self.can_attack = False
                    self.direction = pygame.math.Vector2()

                    if keys[pygame.K_UP]:
                        self.create_attack('top')
                    elif keys[pygame.K_DOWN]:
                        self.create_attack('bottom')
                    else:
                        self.create_attack(self.status.split('_')[0])

                # Jump
                if keys[pygame.K_SPACE] and (self.on_floor or self.can_double_jump):
                    if self.on_floor:
                        self.timers['double jump'].activate()
                    self.can_double_jump = False
                    self.direction.y = -self.jump_speed
                    self.frame_index = 0
                    self.create_particules('before_jump', self.rect.topleft)

                # Dash
                if keys[pygame.K_RCTRL] and self.can_dash:
                    self.direction.y = 0
                    self.can_dash = False
                    self.timers['dash'].activate()
                    self.vulnerable = False
                    self.speed *= 4

            else:
                axis = self.joysticks[0].get_axis(0)
                if abs(axis) < 0.3:
                    axis = 0

                # Movement
                if axis > 0:
                    self.direction.x = axis
                    self.status = 'right'
                elif axis < 0:
                    self.direction.x = axis
                    self.status = 'left'
                else:
                    self.direction.x = 0

                # Attack
                if self.joysticks[0].get_button(2) and self.can_attack:
                    self.timers['attacking'].activate()
                    self.speed_animation = 4 * 3
                    self.frame_index = 0
                    self.can_attack = False
                    self.direction = pygame.math.Vector2()

                    if axis != 0:
                        self.create_attack(self.status.split('_')[0])
                    else:
                        axis = self.joysticks[0].get_axis(1)
                        if abs(axis) < 0.3:
                            axis = 0

                        if axis < 0:
                            self.create_attack('top')
                        elif axis > 0:
                            self.create_attack('bottom')

                # Jump
                if self.joysticks[0].get_button(0) and (self.on_floor or self.can_double_jump):
                    if self.on_floor:
                        self.timers['double jump'].activate()
                    self.can_double_jump = False
                    self.direction.y = -self.jump_speed
                    self.frame_index = 0
                    self.create_particules('before_jump', self.rect.topleft)

                # Dash
                if self.joysticks[0].get_button(5) and self.can_dash:
                    self.direction.y = 0
                    self.can_dash = False
                    self.timers['dash'].activate()
                    self.vulnerable = False
                    self.speed *= 4

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # Movement
        if self.direction.y < 0:
            self.status = self.status.split('_')[0] + '_jump'
        elif self.direction.y > 1:
            self.status = self.status.split('_')[0] + '_fall'
        else:
            if self.direction.x != 0:
                self.status = self.status.split('_')[0] + '_run'

        # Attacking
        if self.timers['attacking'].active:
            self.status = self.status.split('_')[0] + '_attack'

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
                        self.create_particules('after_jump', self.rect.topleft)
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

    def stop_attack(self):
        self.timers['reset attack'].activate()
        self.speed_animation = 4
        self.destroy_attack()

    def reset_attack(self):
        self.can_attack = True

    def update_timers(self):
        for timer in self.timers.values():  # type: Timer
            timer.update()

    def update(self, dt: float):
        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)
