from math import sin
from os import walk
from pathlib import Path

import pygame


def import_folder(path: Path) -> list[pygame.Surface]:
    surface_list = []

    for _, __, img_files in walk(path):
        for image in sorted(img_files):
            full_path = path / image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def wave_value():
    value = sin(pygame.time.get_ticks())
    if value >= 0:
        return 255
    else:
        return 0
