import pygame

from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS


class Transition:
    def __init__(self, reset_player, stop_respawn):
        # setup
        self.display_surface = pygame.display.get_surface()
        self.reset = reset_player
        self.stop = stop_respawn

        # overlay image
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = -2

    def play(self, dt: float):
        self.color += self.speed * dt * TARGET_FPS
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.reset()
        if self.color > 255:
            self.color = 255
            self.speed = -2
            self.stop()

        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
