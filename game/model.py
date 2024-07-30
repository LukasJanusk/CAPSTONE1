import pygame
import player
import level
import enemies
import AI


class Model:
    def __init__(self):
        self.character = player.char
        self.enemies = []
        self.level: level.Level = None
        self.objects = []
    # behaviour setters input and AI
    # interaction between objects

    # updates based on interactions
    def update_player_frame(self):
        self.character.current_time = pygame.time.get_ticks()
        if self.character.current_time - self.character.last_update >= self.character.frame_rate:
            self.character.frame += 1
            self.character.last_update = self.character.current_time

    def update_enemies_frame(self):
        for enemy in self.enemies:
            if enemy.exist:
                enemy.current_time = pygame.time.get_ticks()
                if enemy.current_time - enemy.last_update >= enemy.frame_rate:
                    enemy.frame += 1
                    enemy.last_update = enemy.current_time
                enemy.update_frames()

    def update_enemies_states(self):
        for enemy in self.enemies:
            enemy.update_states()

    def update_enemies_existance(self):
        for enemy in self.enemies:
            if enemy.health <= 0:
                enemy.dead = True
                enemy.idle = False
                enemy.hit = False
                enemy.attacking = False
                enemy.guarding = False
                enemy.stunned = False

    def update_enemies(self):
        self.update_enemies_existance()
        self.update_enemies_states()
        self.update_enemies_frame()

    def update_scroll(self):
        