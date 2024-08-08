import pygame
import sys
from typing import Union, List
import random
from . import player
from . import level
from . import controller
from . import ui
from . import user
from . import menu
from . import enemies
from . import layer
from . import settings
from . import ai
from . import sound
from .particles import Circle, blood_colours
from .sound import (
    attack_normal_sound1,
    attack_normal_sound2,
    attack_upper_sound1,
)


class Model:
    def __init__(self):
        self.user: user.User = user.User("test")
        self.menu_manager: menu.Menu_Controller = menu.menu_controller
        self.character: player.Player = player.char
        self.current_level: level.Level = None
        self.controller: controller.Controller = controller.player_input_manager
        self.settings: settings.Settings = settings.settings
        self.in_menu: bool = True
        self.in_game: bool = False
        self.particles: list = []
        self.sounds: list = []

    # @property
    # def particles(self):
    #     return self._particles

    # @particles.setter
    # def particles(self, value):
    #     # if (not isinstance(value, list)
    #     #     or not all(isinstance(
    #     #         item, (particles.Circle, particles.Line, particles.Particle)) for item in value)):
    #     #     raise TypeError("Trying to add non-particle items to particle items list")
    #     if len(self._particles) + len(value) <= 650:
    #         self._particles += value

    def save_and_quit(self):
        self.user.save()
        self.settings.save()
        pygame.quit()
        sys.exit()

    def load_user(self) -> bool:
        if self.user.load():
            self.settings.load()
            self.update_setting_buttons()
            return True

    def pause_game(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.in_game = False
                self.in_menu = True
                self.menu_manager.current_menu = menu.pause_menu
                pygame.event.clear()

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
            self.play_level_sounds()
        if messege == "continue":
            self.in_menu = False
            self.in_game = True
            pygame.event.clear()
        if messege == "reset":
            self.current_level.current_wave = 0
            self.current_level.current_wave_enemies = []
            self.current_level.score = 0
            self.character.health = self.character.maximum_health
            self.character.x = 100
            self.character.y = 400
        if messege == "score":
            self.set_highscore()
            self.user.save()
            self.current_level.current_wave = 0
            self.current_level.current_wave_enemies = []
            self.current_level.score = 0
            self.character.health = self.character.maximum_health
            self.character.x = 100
            pygame.event.clear()
        if messege == "fps":
            self.settings.draw_fps = True
            if self.settings.draw_fps is True:
                menu.draw_fps_button.NAME = "DRAW FPS -------------------------- ON "
            else:
                menu.draw_fps_button.NAME = "DRAW FPS -------------------------- OFF"
        if messege == "healthbar":
            self.settings.draw_health_bar = True
            if self.settings.draw_health_bar is True:
                menu.draw_monsters_healthbars_button.NAME = "DRAW MONESTER HEALTHABARS --------- ON "
            else:
                menu.draw_monsters_healthbars_button.NAME = "DRAW MONESTER HEALTHABARS --------- OFF"
        if messege == "particles":
            self.settings.render_particles = True
            if self.settings.render_particles is True:
                menu.render_particles_button.NAME = "RENDER PARTICLES ------------------ ON "
            else:
                menu.render_particles_button.NAME = "RENDER PARTICLES ------------------ OFF"
        if messege == "hitboxes":
            self.settings.draw_hitboxes = True
            if self.settings.draw_hitboxes is True:
                menu.draw_hitboxes_button.NAME = "DRAW HITBOXES --------------------- ON "
            else:
                menu.draw_hitboxes_button.NAME = "DRAW HITBOXES --------------------- OFF"

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

    def get_current_level_wave(self, print_info=False) -> bool:
        if (len(self.current_level.current_wave_enemies) < 1
                or self.current_level.current_wave_enemies is None):
            self.current_level.current_wave_enemies = self.current_level.generate_wave(self.character.x)
            if (self.current_level.current_wave_enemies is None
                    or len(self.current_level.current_wave_enemies) == 0):
                if print_info:
                    print("Failed to create new wave for current level")
                return False
            else:
                if print_info:
                    print(
                        f"Wave of {len(self.current_level.current_wave_enemies)} enemies generated")
                return True

    def run_enemies_ai(self):
        for enemy in self.current_level.current_wave_enemies:
            if type(enemy) is enemies.Demon:
                ai.DemonAI.choose_action(enemy, self.character)
            if type(enemy) is enemies.Imp:
                ai.ImpAI.choose_action(enemy, self.character)

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
                        if type(enemy) is enemies.Demon:
                            enemy.stun_threshold -= damage
                            if enemy.stun_threshold == 0 or damage > 200:
                                enemy.hit = True
                                enemy.frame = 0
                        else:
                            enemy.frame = 0
                            enemy.hit = True
                    if print_damage:
                        print(f"Player dealt {damage} damage to ", end="")
                        print(enemy)
                    particle_generation_rect = Model.get_collision_rect(
                        self.character.current_attack.hitbox,
                        enemy.hitbox
                        )
                    particle_generation_position = Model.get_random_position_in_rect(
                        particle_generation_rect
                        )
                    if type(enemy) is enemies.Demon:
                        particles_n = random.randint(7, 10)
                        particles_size = random.randint(3, 5)
                    if type(enemy) is enemies.Imp:
                        particles_n = random.randint(7, 10)
                        particles_size = random.randint(2, 4)
                    if len(self.particles) < 400:
                        list = Circle.generate_cicles(
                            particles_n,
                            random.choice(blood_colours),
                            particle_generation_position,
                            self.character.facing_right,
                            radius=particles_size,
                            speed=random.randint(4, 5))
                        self.particles += list

    def enemies_attack(self, print_damage: bool = False):
        for enemy in self.current_level.current_wave_enemies:
            if enemy.attacking:
                damage = enemy.attack.hit(enemy.frame, self.character.hitbox)
                if damage:
                    # if self.character.guarding:
                    #     self.character.health -= int(damage / 2)
                    if not self.character.guarding:
                        self.character.health -= int(damage)
                    self.character.hit = True
                    self.character.frame = 0
                    if print_damage:
                        print(f"Player received {damage} damage from ", end="")
                        print(enemy)

    def update_player(self):
        self.character.reset_frames()
        self.character.update_speed()
        self.character.update_hitbox()
        self.character.update_jumping()
        self.character.get_current_animation()
        self.character.get_current_attack()
        if self.character.current_attack is not None:
            self.character.current_attack.update_hitbox(
                self.character.x,
                self.character.y,
                self.character.facing_right
                )
        self.update_player_frame()

    def get_layers_for_blit(self) -> List[
        Union[
            ui.Score,
            ui.Healthbar,
            layer.Layer,
            player.Player,
            enemies.Enemy,
            enemies.Demon,
            enemies.Imp]
            ]:
        layers = [
            self.current_level.layer0,
            self.current_level.layer1,
            self.current_level.layer2,
            self.current_level.layer3,
            self.current_level.layer4,
            self.current_level.layer5] + (
            self.current_level.current_wave_enemies +
            [self.character] +
            self.particles +
            [self.current_level.layer6,
             self.current_level.layer7] +
            [ui.health_bar] +
            [ui.score]
            )
        return layers

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

    def update_enemies_existance(self, print_info=False):
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
                        self.current_level.score += 30
                    self.current_level.current_wave_enemies.remove(enemy)
                    if print_info:
                        print(f"Enemy , {enemy}, removed from the active enemies list")

    def check_for_level_end(self):
        if ((self.current_level.current_wave == self.current_level.total_waves
                and len(self.current_level.current_wave_enemies) < 1)
                or self.character.health == 0):
            self.in_game = False
            self.in_menu = True
            self.menu_manager.current_menu = menu.score_menu
            self.menu_manager.current_menu.name = "SCORE:" + str(self.current_level.score)
            self.menu_manager.current_menu.update_surface()

    def update_layer_scroll(self):
        layers_list = self.current_level.get_layers_list()
        for layer_item in layers_list:
            if layer_item is not None:
                layer_current_scroll = (
                    layer_item.scroll + self.character.speed) * layer_item.scroll_multiplier
                layer_item.distance += layer_current_scroll
                if abs(layer_item.distance) > layer_item.width:
                    layer_item.distance = 0
        for enemy_obj in self.current_level.current_wave_enemies:
            if len(self.current_level.current_wave_enemies) > 0:
                enemy_obj.x += self.character.speed
        for particle in self.particles:
            x, y = particle.position
            x += self.character.speed
            particle.position = (x, y)

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
                for particle in self.particles:
                    x, y = particle.position
                    x -= 0.5
                    particle.position = (x, y)
        if not self.character.facing_right:
            if self.character.x < 390:
                self.character.x += 0.5
                for layer_item in layers_list:
                    if layer_item is not None:
                        layer_item.distance += (0.5 * layer_item.scroll_multiplier)
                for enemy in self.current_level.current_wave_enemies:
                    enemy.x += 0.5
                for particle in self.particles:
                    x, y = particle.position
                    x += 0.5
                    particle.position = (x, y)

    @staticmethod
    def get_random_position_in_rect(rect: pygame.rect.Rect) -> tuple:
        x = random.randint(rect.x, rect.x + rect.width)
        y = random.randint(rect.y, rect.y + rect.height)
        return (x, y)

    @staticmethod
    def get_collision_rect(
        rect1: pygame.rect.Rect,
        rect2: pygame.rect.Rect
            ) -> pygame.rect.Rect:
        if rect1.colliderect(rect2):
            return rect1.clip(rect2)
        return None

    def update_particles(self):
        for particle in self.particles:
            if type(particle) is Circle:
                particle.update_position()
                particle.decrease_size(0.05)
                x, y = particle.position
                if particle.update_existance() is False:
                    self.particles.remove(particle)
                elif y >= 560:
                    maybe = random.choice([True, False])
                    if maybe and len(self.particles) < 400:
                        list = Circle.generate_cicles(
                            1,
                            random.choice(blood_colours),
                            particle.position,
                            random.choice([True, False]),
                            random.randint(1, 3),
                            speed=(random.randint(10, 100)/100))
                        self.particles += list
                    self.particles.remove(particle)

    def print_particles_n(self):
        print(len(self.particles))

    def update_setting_buttons(self):
        if self.settings.draw_fps is True:
            menu.draw_fps_button.NAME = "DRAW FPS -------------------------- ON "
        else:
            menu.draw_fps_button.NAME = "DRAW FPS -------------------------- OFF"
        if self.settings.draw_health_bar is True:
            menu.draw_monsters_healthbars_button.NAME = "DRAW MONESTER HEALTHABARS --------- ON "
        else:
            menu.draw_monsters_healthbars_button.NAME = "DRAW MONESTER HEALTHABARS --------- OFF"
        if self.settings.render_particles is True:
            menu.render_particles_button.NAME = "RENDER PARTICLES ------------------ ON "
        else:
            menu.render_particles_button.NAME = "RENDER PARTICLES ------------------ OFF"
        if self.settings.draw_hitboxes is True:
            menu.draw_hitboxes_button.NAME = "DRAW HITBOXES --------------------- ON "
        else:
            menu.draw_hitboxes_button.NAME = "DRAW HITBOXES --------------------- OFF"

    @staticmethod
    def get_attack_sound(
            attacker: player.Player | enemies.Enemy | enemies.Demon | enemies.Imp,
            ) -> sound.HitSound:
        current_time = pygame.time.get_ticks()
        if type(attacker) is player.Player:
            last_update = attacker.current_attack.sound.last_update
            downtime = attacker.current_attack.sound.DOWNTIME
        if (type(attacker) is enemies.Demon or
                type(attacker) is enemies.Imp or
                type(attacker) is enemies.Enemy):
            last_update = attacker.attack.sound.last_update
            downtime = attacker.attack.sound.DOWNTIME
        if current_time - last_update > downtime:
            if type(attacker) is player.Player:
                attacker.current_attack.sound.last_update = current_time
                return attacker.current_attack.sound
            if (type(attacker) is enemies.Demon or
                    type(attacker) is enemies.Imp or
                    type(attacker) is enemies.Enemy):
                attacker.attack.sound.last_update = current_time
                return attacker.attack.sound

    @staticmethod
    def get_hit_sound(object: player.Player | enemies.Enemy | enemies.Imp | enemies.Demon):
        current_time = pygame.time.get_ticks()
        downtime_hit = object.hit_sound.DOWNTIME
        last_update_hit = object.hit_sound.last_update
        if current_time - last_update_hit > downtime_hit:
            object.hit_sound.last_update = current_time
            return object.hit_sound

    def get_attack_sounds(self):
        attack_sounds = []
        for enemy in self.current_level.current_wave_enemies:
            if enemy.attacking:
                if enemy.attack.hit(enemy.frame, self.character.hitbox):
                    sound = Model.get_attack_sound(enemy)
                    hit_sound = Model.get_hit_sound(self.character)
                    attack_sounds.append(sound)
                    attack_sounds.append(hit_sound)
            if self.character.current_attack is not None:
                if self.character.current_attack.hit(self.character.frame, enemy.hitbox):
                    player_attack_sound = Model.get_attack_sound(self.character)
                    hit_sound = Model.get_hit_sound(enemy)
                    attack_sounds.append(player_attack_sound)
                    attack_sounds.append(hit_sound)
        if len(attack_sounds) == 0:
            return []
        else:
            return attack_sounds

    def play_level_sounds(self):
        if self.current_level is not None:
            self.current_level.ambient_sound.play(loops=-1)

    def get_animation_sound(self):
        if self.character.attacking_normal:
            if self.character.frame == attack_normal_sound1.frame:
                return attack_normal_sound1
            if self.character.frame == attack_normal_sound2.frame:
                return attack_normal_sound2
        if self.character.attacking_upper:
            if self.character.frame == attack_upper_sound1.frame:
                return attack_upper_sound1

    def get_sounds(self):
        if len(self.sounds) > 200:
            self.sounds = self.sounds[:-30]
        sounds = []
        animation_sound = self.get_animation_sound()
        if animation_sound:
            sounds.append(animation_sound)
        hit_sounds = self.get_attack_sounds()
        sounds += hit_sounds
        return sounds
