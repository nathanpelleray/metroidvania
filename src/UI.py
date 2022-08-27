import pygame

from src.player import Player
from src.settings import BASE_DIR


class UI:
    def __init__(self):
        # Setup
        self.display_surface = pygame.display.get_surface()

        # Surfaces
        self.full_heart_surf = pygame.image.load(BASE_DIR / "graphics" / "heart" / "hearts_hud.png").convert_alpha()
        self.empty_heart_surf = pygame.image.load(BASE_DIR / "graphics" / "heart" / "no_hearts_hud.png").convert_alpha()

    def draw(self, player: Player):
        for i in range(player.max_health):
            if (i + 1) <= player.health:
                full_heart_rect = pygame.Rect((10 * i) + (self.full_heart_surf.get_width() * i), 10,
                                              self.full_heart_surf.get_width(), self.full_heart_surf.get_height())
                self.display_surface.blit(self.full_heart_surf, full_heart_rect)
            else:
                empty_hearth_rect = pygame.Rect((10 * i) + (self.empty_heart_surf.get_width() * i), 10,
                                                self.empty_heart_surf.get_width(), self.empty_heart_surf.get_height())
                self.display_surface.blit(self.empty_heart_surf, empty_hearth_rect)
