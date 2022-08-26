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
