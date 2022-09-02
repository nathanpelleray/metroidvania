import sys

import pygame

from src.level import Level
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FULLSCREEN


class Game:
    def __init__(self):
        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        if FULLSCREEN:
            self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()),
                                                  pygame.FULLSCREEN)
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()

        # Joystick
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        self.level = Level(self.joysticks)

    def run(self):
        while True:
            # FPS
            dt = self.clock.tick(FPS) / 1000

            # Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.joystick.quit()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.JOYDEVICEADDED:
                    self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
                    self.level.change_joysticks(self.joysticks)
                if event.type == pygame.JOYDEVICEREMOVED:
                    self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
                    self.level.change_joysticks(self.joysticks)

            # Updates
            self.level.run(dt)
            pygame.display.update()
