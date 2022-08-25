import pygame
import sys

from level import Level
from settings import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()

level = Level()

while True:
    dt = clock.tick(FPS) / 1000
    print(dt)

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)
    level.run(dt)

    # drawing logic
    pygame.display.update()
