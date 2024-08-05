import pygame
import sys
from . import player
from . import level
from . import controller
from . import ui
from . import user
from . import menu
from . import enemies


class Model:
    def __init__(self):
        self.user: user.User = user.User("test")
        self.menu_manager: menu.Menu_Controller = menu.menu_controller
        self.character: player.Player = player.char
        self.current_level: level.Level = None
        self.controller: controller.Controller = controller.player_input_manager
        self.in_menu: bool = True
        self.pause: bool = False
        self.in_game: bool = False

    def save_and_quit(self):
        self.user.save_user()
        pygame.quit()
        sys.exit()

    def load_user(self):
        self.user.load_user()

    def pause_game(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.in_game = False
                self.in_menu = True
                self.menu_manager.current_menu = menu.pause_menu

    def run_menus(self, event: pygame.event.Event):
        self.menu_manager.get_active_button(event)
        messege = self.menu_manager.set_active_menu(event)
        if messege == "quit":
            self.save_and_quit()
        if messege == "level1":
            self.in_menu = False
            self.in_game = True
            self.current_level = level.level1
        if messege == "level2":
            self.in_menu = False
            self.in_game = True
            self.current_level = level.level2
        if messege == "level3":
            self.in_menu = False
            self.in_game = True
            self.current_level = level.level3
        if messege == "continue":
            self.in_menu = False
            self.in_game = True
        if messege == "reset":
            self.current_level.current_wave = 0
            self.current_level.current_wave_enemies = []
            self.current_level.score = 0
            self.character.health = self.character.maximum_health
            self.character.x = 100
        if messege == "score":
            self.set_highscore()
            self.user.save_user()
            self.current_level.current_wave = 0
            self.current_level.current_wave_enemies = []
            self.current_level.score = 0
            self.character.health = self.character.maximum_health
            self.character.x = 100

    def set_highscore(self):
        if self.current_level == level.level1:
            self.user.level1_highscore = self.current_level.score
        if self.current_level == level.level2:
            self.user.level2_highscore = self.current_level.score
        if self.current_level == level.level3:
            self.user.level3_highscore = self.current_level.score
        # if self.current_level == level.level4:
        #     self.user.level4_highscore = self.current_level.score
        # if self.current_level == level.level5:
        #     self.user.level5_highscore = self.current_level.score

    def get_current_level_wave(self):
        if len(self.current_level.current_wave_enemies) < 1 or self.current_level.current_wave_enemies is None:
            self.current_level.current_wave_enemies = self.current_level.generate_wave(self.character.x)
            # print("Wave generated")
            # print(f"{len(self.current_level.current_wave_enemies)}")

    def update_enemies(self):
        self.update_enemies_existance()
        self.update_enemies_states()
        self.update_enemies_frame()
        self.update_enemies_hitboxes()
        self.update_enemies_attacks_hitboxes()

    def update_enemies_attacks_hitboxes(self):
        for enemy in self.current_level.current_wave_enemies:
            if enemy.attack is not None:
                enemy.attack.update_hitbox(enemy.x, enemy.y, enemy.facing_right)

    def update_enemies_hitboxes(self):
        for enemy in self.current_level.current_wave_enemies:
            enemy.update_hitbox()

    def update_scroll(self):
        self.update_layer_scroll()
        self.update_camera()

    def get_player_input(self, event: pygame.event.Event):
        self.controller.get_player_key_events(event)

    def calculate_attacks(self, print_damage: bool = False):
        self.player_attack(print_damage=print_damage)
        self.enemies_attack(print_damage=print_damage)

    def player_attack(self, print_damage=False):
        if self.character.current_attack is not None:
            for enemy in self.current_level.current_wave_enemies:
                damage = self.character.current_attack.hit(self.character.frame, enemy.hitbox)
                if damage:
                    enemy.health -= damage
                    if not enemy.dead:
                        enemy.hit = True
                        enemy.frame = 0
                    if print_damage:
                        print(f"Player dealt {damage} damage to ", end="")
                        print(enemy)

    def enemies_attack(self, print_damage=False):
        for enemy in self.current_level.current_wave_enemies:
            if enemy.attacking:
                damage = enemy.attack.hit(enemy.frame, self.character.hitbox)
                if damage:
                    if self.character.guarding:
                        self.character.health -= int(damage / 2)
                    else:
                        self.character.health -= int(damage)
                    self.character.hit = True
                    self.character.frame = 0
                    if print_damage:
                        print(f"Player received {damage} damage from ", end="")
                        print(enemy)

    def update_player(self):
        # interaction between objects and enemies update
        self.character.reset_frames()
        self.character.update_speed()
        self.character.update_hitbox()
        self.character.update_jumping()
        self.character.get_current_animation()
        self.character.get_current_attack()
        if self.character.current_attack is not None:
            self.character.current_attack.update_hitbox(self.character.x, self.character.y, self.character.facing_right)
        self.update_player_frame()

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
                  self.current_level.layer7] +
                 [ui.health_bar] +
                 [ui.score]
                  )
        return layers

    def get_objects_for_render(self):
        objects = []
        return objects

    def update_player_frame(self):
        self.character.current_time = pygame.time.get_ticks()
        if self.character.current_time - self.character.last_update >= self.character.frame_rate:
            self.character.frame += 1
            self.character.last_update = self.character.current_time

    def update_enemies_frame(self):
        for enemy in self.current_level.current_wave_enemies:
            if enemy.exist:
                current_time = pygame.time.get_ticks()
                if current_time - enemy.last_update >= enemy.frame_rate:
                    enemy.frame += 1
                    enemy.last_update = current_time
                enemy.reset_frames()

    def update_enemies_states(self):
        for enemy in self.current_level.current_wave_enemies:
            enemy.update_states()

    def update_enemies_existance(self):
        for enemy in self.current_level.current_wave_enemies:
            if enemy.health <= 0:
                enemy.dead = True
                enemy.idle = False
                enemy.hit = False
                enemy.attacking = False
                enemy.guarding = False
                enemy.stunned = False
                if enemy.exist is False:
                    if type(enemy) is enemies.Demon:
                        self.current_level.score += 100
                    if type(enemy) is enemies.Imp:
                        self.current_level.score += 10
                    self.current_level.current_wave_enemies.remove(enemy)

    def check_for_level_end(self):
        if self.current_level.current_wave == self.current_level.waves and len(self.current_level.current_wave_enemies) < 1:
            self.in_game = False
            self.in_menu = True
            self.menu_manager.current_menu = menu.score_menu
            self.menu_manager.current_menu.name = "SCORE:" + str(self.current_level.score)
            self.menu_manager.current_menu.update_surface()

    def update_layer_scroll(self):
        layers_list = self.current_level.get_layers_list()
        for layer_item in layers_list:
            if layer_item is not None:
                layer_current_scroll = (layer_item.scroll + self.character.speed) * layer_item.scroll_multiplier
                layer_item.distance += layer_current_scroll
                if abs(layer_item.distance) > layer_item.width:
                    layer_item.distance = 0
        for enemy_obj in self.current_level.current_wave_enemies:
            if len(self.current_level.current_wave_enemies) > 0:
                enemy_obj.x += self.character.speed

    def update_camera(self):
        layers_list = self.current_level.get_layers_list()
        if self.character.facing_right:
            if self.character.x > 220:
                self.character.x -= 0.5
                for layer_item in layers_list:
                    if layer_item is not None:
                        layer_item.distance -= (0.5 * layer_item.scroll_multiplier)
                for enemy in self.current_level.current_wave_enemies:
                    enemy.x -= 0.5
        if not self.character.facing_right:
            if self.character.x < 390:
                self.character.x += 0.5
                for layer_item in layers_list:
                    if layer_item is not None:
                        layer_item.distance += (0.5 * layer_item.scroll_multiplier)
                for enemy in self.current_level.current_wave_enemies:
                    enemy.x += 0.5
