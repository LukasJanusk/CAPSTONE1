import pygame
import player
import level
import enemies
import AI


class Model:
    def __init__(self):
        self.character = player.char
        self.current_level: level.Level = None

    # behaviour setters input and AI
    # interaction between objects

    # updates based on interactions
    def get_layers_for_blit(self):
        layers = [self.current_level.layer0,
                  self.current_level.layer1,
                  self.current_level.layer2,
                  self.current_level.layer3,
                  self.current_level.layer4,
                  self.current_level.layer5] + (
                  self.current_level.current_wave_enemies +
                 [self.character] +
                 [self.current_level.layer6,
                  self.current_level.layer7])
        return layers

    def update_layer_scroll(self):
        layers_list = self.current_level.get_layers_list
        for layer_item in layers_list:
            if layer_item is not None:
                layer_current_scroll = layer_item.scroll + self.character.speed
                layer_item.distance += layer_current_scroll
        for enemy_obj in self.current_level.current_wave_enemies:
            if len(self.current_level.current_wave_enemies) > 0:
                enemy_obj.x += self.character.speed

    def update_player_frame(self):
        self.character.current_time = pygame.time.get_ticks()
        if self.character.current_time - self.character.last_update >= self.character.frame_rate:
            self.character.frame += 1
            self.character.last_update = self.character.current_time

    def update_enemies_frame(self):
        for enemy in self.current_level.current_wave_enemies:
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
                self.current_level.current_wave_enemies.remove(enemy)

    def update_enemies(self):
        self.update_enemies_existance()
        self.update_enemies_states()
        self.update_enemies_frame()

    def update_scroll(self):
        self.update_layer_scroll()
        self.update_camera()

    def update_player_speed(self):
        if not self.character.jumping:
            self.character.aerial_movement = False
        self.character.speed = 0
        if self.character.running is True:
            self.character.speed += 2.5
        if self.character.walking is True:
            self.character.speed += 1.5
        if self.character.dashing:
            self.character.speed += 4
        if self.character.attack_moving is True:
            self.character.speed += 0.4
        if self.character.aerial_movement is True:
            self.character.speed += 2
        if self.character.ducking is True:
            self.character.speed = 0
        if self.character.guarding is True:
            self.character.speed = 0
        if self.character.idle is True:
            self.character.speed = 0
        if self.character.facing_right:
            self.character.speed = self.character.speed * -1

    def update_camera(self):
        layers_list = self.current_level.get_layers_list()
        if self.character.facing_right:
            if self.character.x > 220:
                self.character.x -= 0.5
                for layer_item in layers_list:
                    layer_item.distance -= 0.5
                for enemy in self.enemies:
                    enemy.x -= 0.5
        if not self.character.facing_right:
            if self.character.x < 390:
                self.character.x += 0.5
                for layer_item in layers_list:
                    layer_item.distance += 0.5
                for enemy in self.enemies:
                    enemy.x += 0.5
