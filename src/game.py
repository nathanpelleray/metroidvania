import sys

import pygame

from src.level import Level
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class Game:
    def __init__(self):
        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            # FPS
            dt = self.clock.tick(FPS) / 1000

            # Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Updates
            self.level.run(dt)
            pygame.display.update()
