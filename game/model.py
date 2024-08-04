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

    def run_menus(self, event: pygame.event.Event):
        self.menu_manager.get_active_button(event)
        messege = self.menu_manager.set_active_menu(event)
        if messege == "quit":
            self.save_and_quit()
        if messege == "level3":
            self.in_menu = False
            self.in_game = True
            self.current_level = level.level3

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

    def calculate_attacks(self):
        self.player_attack()
        self.enemies_attack()

    def player_attack(self):
        if self.character.current_attack is not None:
            for enemy in self.current_level.current_wave_enemies:
                damage = self.character.current_attack.hit(self.character.frame, enemy.hitbox)
                if damage:
                    enemy.health -= damage
                    enemy.hit = True
                    print(f"Player dealt {damage} damage")

    def enemies_attack(self):
        for enemy in self.current_level.current_wave_enemies:
            if enemy.attacking:
                damage = enemy.attack.hit(enemy.frame, self.character.hitbox)
                if damage:
                    self.character.health -= damage
                    print(f"Player received {damage}")

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
                 [ui.health_bar.draw_health_bar()] +
                 [ui.score.get_score_surface(str(self.current_level.score))]
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
                    if enemy is enemies.Demon:
                        self.current_level.score += 100
                    if enemy is enemies.Imp:
                        self.current_level.score += 10
                    self.current_level.current_wave_enemies.remove(enemy)

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
