import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], surf: pygame.Surface, groups: list[pygame.sprite.AbstractGroup]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class AnimatedTile(Tile):
    def __init__(self, pos: tuple[int, int], frames: list[pygame.Surface],
                 groups: list[pygame.sprite.AbstractGroup], speed_animation: int = 5):
        # Animation
        self.frames = frames
        self.frame_index = 0
        self.speed_animation = speed_animation

        # Setup
        super().__init__(
            pos=pos,
            surf=self.frames[self.frame_index],
            groups=groups
        )

    def animate(self, dt: float):
        self.frame_index += self.speed_animation * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt: float):
        self.animate(dt)
