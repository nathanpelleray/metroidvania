import pygame
from pytmx import load_pygame

from src.UI import UI
from src.camera import CameraGroup
from src.enemy import Enemy
from src.level_data import LEVELS
from src.particule import ParticuleManager
from src.player import Player
from src.settings import TILE_SIZE, BG_COLOR, BASE_DIR, DEBUG, LAYERS
from src.support import import_folder
from src.tile import Tile, AnimatedTile, ExitTile, Checkpoint
from src.timer import Timer
from src.transition import Transition
from src.weapon import Weapon


class Level:
    def __init__(self):
        # Setup
        self.display_surface = pygame.display.get_surface()

        # Groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.collider_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.checkpoint_sprites = pygame.sprite.Group()
        self.exit_sprites = pygame.sprite.Group()
        self.last_checkpoint = None
        self.current_attack = None

        # Timers
        self.timers = {
            'screen shake': Timer(300, self.stop_screen_shake),
            'player death': Timer(1500, self.death_animation)
        }

        # Screen Shake
        self.screen_shake = False

        # Player
        self.player = Player((128, 576), self.all_sprites, self.collision_sprites, self.create_attack,
                             self.destroy_attack, self.create_particules)
        self.respawn = False

        # Map
        self.current_level = 'map_test'
        self.load_map(self.current_level)

        # User interface
        self.ui = UI()

        # Particules
        self.particule_manager = ParticuleManager()

        # Transition
        self.transition = Transition(self.reset_player, self.stop_respawn)

    def load_map(self, level_name, x: int = None, y: int = None):
        self.clear_map()
        tmx_data = load_pygame(f'data/{level_name}.tmx')
        self.current_level = level_name

        if x and y:
            self.player.pos.x = x
            self.player.pos.y = y

        # Terrain
        for x, y, surf in tmx_data.get_layer_by_name('Terrain').tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), [self.all_sprites, self.collision_sprites], surf, LAYERS['terrain'])

        # Water
        water_frames = import_folder(BASE_DIR / "graphics" / "water")
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            AnimatedTile((x * TILE_SIZE, y * TILE_SIZE), water_frames, [self.all_sprites], z=LAYERS['water'], alpha=150)

        # Enemies
        for obj in tmx_data.get_layer_by_name('Enemies'):
            if obj.name == 'Collider':
                Tile((obj.x, obj.y), [self.collider_sprites], z=LAYERS['invisible'])
            if obj.type == 'Enemy':
                Enemy(obj.name, (obj.x, obj.y), [self.all_sprites, self.enemy_sprites], self.collider_sprites,
                      self.create_particules)

        # Interaction
        for obj in tmx_data.get_layer_by_name('Interaction'):
            if obj.name == 'Checkpoint':
                Checkpoint(self.current_level, (obj.x, obj.y), [self.checkpoint_sprites])

        # Exit
        for obj in tmx_data.get_layer_by_name('Exit'):
            ExitTile(self.current_level, obj.name, (obj.x, obj.y), obj.width, obj.height,
                     [self.all_sprites, self.exit_sprites])

    def clear_map(self):
        # Groups
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.collider_sprites.empty()
        self.enemy_sprites.empty()
        self.checkpoint_sprites.empty()
        self.exit_sprites.empty()
        if self.current_attack:
            self.current_attack.kill()

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.all_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.current_attack:
            collision_sprites = pygame.sprite.spritecollide(self.current_attack, self.enemy_sprites, False)
            if collision_sprites:
                for target_sprite in collision_sprites:  # type: Enemy
                    target_sprite.get_damage(self.player)

    def damage_player(self):
        if self.player.vulnerable:
            collision_sprites = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
            if collision_sprites:
                for _ in collision_sprites:
                    self.player.health -= 1
                    self.player.vulnerable = False
                    self.player.timers['invulnerability'].activate()
                    self.screen_shake = True
                    self.timers['screen shake'].activate()

                    if self.player.health <= 0:
                        self.particule_manager.create_particules('player_death', self.player.rect.topleft,
                                                                 self.all_sprites)
                        self.player.kill()
                        self.timers['player death'].activate()

    def reset_player(self):
        self.load_map(self.last_checkpoint.level_name)
        x = self.last_checkpoint.rect.x
        y = self.last_checkpoint.rect.y
        self.player = Player((x, y), self.all_sprites, self.collision_sprites, self.create_attack,
                             self.destroy_attack, self.create_particules)

    def stop_respawn(self):
        self.respawn = False

    def death_animation(self):
        self.respawn = True

    def checkpoint_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self.player, self.checkpoint_sprites, False)
        if collision_sprites:
            for checkpoint in collision_sprites:  # type: Tile
                self.last_checkpoint = checkpoint

    def exit_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self.player, self.exit_sprites, False)
        if collision_sprites:
            for exit_sprite in collision_sprites:  # type: ExitTile
                x = LEVELS[exit_sprite.new_level][exit_sprite.current_level][0]
                y = LEVELS[exit_sprite.new_level][exit_sprite.current_level][1]
                self.load_map(exit_sprite.new_level, x, y)

    def create_particules(self, animation_type: str, pos: tuple[int, int]):
        self.particule_manager.create_particules(animation_type, pos, self.all_sprites)

    def stop_screen_shake(self):
        self.screen_shake = False

    def update_timers(self):
        for timer in self.timers.values():  # type: Timer
            timer.update()

    def run(self, dt: float):
        # Drawing logic
        self.display_surface.fill(BG_COLOR)
        self.all_sprites.custom_draw(self.player, self.screen_shake)
        self.ui.draw(self.player)

        # Debug
        if DEBUG:
            self.all_sprites.draw_debug()

        # Update logic
        self.all_sprites.update(dt)
        self.update_timers()
        self.damage_player()
        self.player_attack_logic()
        self.checkpoint_collision()
        self.exit_collision()

        if self.respawn:
            self.transition.play(dt)
