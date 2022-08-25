import pygame

from src.settings import TILE_SIZE, PLAYER_COLOR, TARGET_FPS


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], group: pygame.sprite.Group,
                 collision_sprites: pygame.sprite.Group):
        super().__init__(group)
        self.image = pygame.Surface((TILE_SIZE // 2, TILE_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)  # Ajout
        self.speed = 8 * TARGET_FPS
        self.gravity = 0.8 * TARGET_FPS
        self.jump_speed = 16
        self.collision_sprites = collision_sprites
        self.on_floor = False

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -self.jump_speed

    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                self.pos.x = self.rect.x

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_floor = True
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

    def update(self, dt: float):
        self.input()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.horizontal_collisions()
        self.apply_gravity(dt)
        self.vertical_collisions()
