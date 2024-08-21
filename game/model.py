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
from .particles import Particle, Circle, Blood, Square, BlockSquare
from .sound import (
    attack_normal_sound1,
    attack_normal_sound2,
    attack_upper_sound1,
    player_block_sound
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

    def save_and_quit(self) -> None:
        """Saves highscores and settings then exits the program"""
        self.user.save()
        self.settings.save()
        pygame.quit()
        sys.exit()

    def load_user(self) -> bool:
        """Loads user data and settings data then updates buttons based on settings"""
        if self.user.load():
            self.settings.load()
            self.update_setting_buttons()
            return True

    def pause_game(self, event: pygame.event.Event) -> None:
        """Pauses the game on ESCAPE press when in game"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.in_game = False
                self.in_menu = True
                self.menu_manager.current_menu = menu.pause_menu
                pygame.event.clear()

    def run_menus(self, event: pygame.event.Event) -> None:
        """Runs menus"""
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
            self.sounds = []
            self.current_level.objects = []
            self.current_level.score = 0
            self.character.health = self.character.maximum_health
            self.character.x = 100
            self.character.y = 400
        if messege == "score":
            self.set_highscore()
            self.user.save()
            self.current_level.current_wave = 0
            self.current_level.current_wave_enemies = []
            self.sounds = []
            self.current_level.objects = []
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

    def set_highscore(self) -> None:
        """Sets highscore once  the current level is finihed"""
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
        """Generates new enemies wave once current one is defeated"""
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

    def run_enemies_ai(self) -> None:
        """Runs AI of enemies"""
        for enemy in self.current_level.current_wave_enemies:
            if type(enemy) is enemies.Demon:
                ai.DemonAI.choose_action(enemy, self.character)
            if type(enemy) is enemies.Imp:
                ai.ImpAI.choose_action(enemy, self.character)

    def update_enemies(self) -> None:
        """Master function for updates of enemies"""
        self.update_enemies_existance()
        self.update_enemies_states()
        self.update_enemies_frame()
        self.update_enemies_hitboxes()
        self.update_enemies_attacks_hitboxes()

    def update_enemies_attacks_hitboxes(self) -> None:
        """Updates hitboxes of enemies attacks"""
        for enemy in self.current_level.current_wave_enemies:
            if enemy.attack is not None:
                enemy.attack.update_hitbox(enemy.x, enemy.y, enemy.facing_right)

    def update_enemies_hitboxes(self) -> None:
        """Updates hitboxes of enemies"""
        for enemy in self.current_level.current_wave_enemies:
            enemy.update_hitbox()

    def update_scroll(self) -> None:
        """Master function for updating objects position on the screen"""
        self.update_layer_scroll()
        self.update_camera()

    def get_player_input(self, event: pygame.event.Event) -> None:
        """Runs player updates based on keyboard input"""
        self.controller.get_player_key_events(event)

    def calculate_attacks(self, print_damage: bool = False) -> None:
        """Master function for calculating attacks"""
        self.player_attack(print_damage=print_damage)
        self.enemies_attack(print_damage=print_damage)

    def player_attack(self, print_damage=False) -> None:
        """Checks if player hit enemies and calculates stun threshold and damage"""
        if self.character.current_attack is not None:
            for enemy in self.current_level.current_wave_enemies:
                damage = self.character.current_attack.hit(self.character.frame, enemy.hitbox)
                if damage:
                    enemy.health -= damage
                    if not enemy.dead:
                        if type(enemy) is enemies.Demon:
                            enemy.stun_threshold -= damage
                            if enemy.stun_threshold == 0 or damage > 200 or enemy.spawn:
                                enemy.hit = True
                                enemy.frame = 0
                        else:
                            enemy.frame = 0
                            enemy.hit = True
                    if print_damage:
                        print(f"Player dealt {damage} damage to ", end="")
                        print(enemy)

    def enemies_attack(self, print_damage: bool = False) -> None:
        """Checks if enemies hit player and calculates damage done"""
        for enemy in self.current_level.current_wave_enemies:
            if enemy.attacking:
                damage = enemy.attack.hit(enemy.frame, self.character.hitbox)
                if damage:
                    if not self.character.guarding:
                        self.character.health -= int(damage)
                    self.character.hit = True
                    self.character.frame = 0
                    if print_damage:
                        print(f"Player received {damage} damage from ", end="")
                        print(enemy)

    def generate_particles(self) -> None:
        """Master function for particle generation"""
        self.generate_blood_particles()
        self.generate_block_particles()

    def generate_blood_particles(self) -> None:
        """Generates blood particles on hit and bounce of the ground"""
        particles = []
        if self.character.current_attack is not None:
            for enemy in self.current_level.current_wave_enemies:
                if self.character.current_attack.hit(self.character.frame, enemy.hitbox):
                    if not enemy.dead:
                        particle_generation_rect = Particle.get_collision_rect(
                            self.character.current_attack.hitbox,
                            enemy.hitbox
                            )
                        particle_generation_position = Particle.get_random_position_in_rect(
                            particle_generation_rect
                            )
                        if type(enemy) is enemies.Demon:
                            particles_n = random.randint(10, 12)
                            particles_size = 5
                        if type(enemy) is enemies.Imp:
                            particles_n = random.randint(10, 12)
                            particles_size = 3
                        if len(self.particles) < 400:
                            list = Blood.generate_blood(
                                particles_n,
                                particle_generation_position,
                                particles_size,
                                2,
                                facing_right=self.character.facing_right
                            )
                            particles += list
            for particle in self.particles:
                if type(particle) is Blood:
                    x, y = particle.position
                    if y >= 560:
                        if len(self.particles) < 400:
                            splash_list = Blood.generate_blood_splash(
                                particle.position,
                                particle.radius
                            )
                            particles += splash_list
                        self.particles.remove(particle)
        self.particles += particles

    def generate_block_particles(self) -> None:
        """Generates block particles for render on player block"""
        particles = []
        if self.character.guarding and len(self.particles) < 450:
            for enemy in self.current_level.current_wave_enemies:
                if enemy.attacking:
                    if enemy.attack.hit(enemy.frame, self.character.hitbox):
                        rect = Particle.get_collision_rect(enemy.attack.hitbox, self.character.hitbox)
                        position = Particle.get_random_position_in_rect(rect)
                        block_squares = BlockSquare.generate_block_squares(5, position, 15)
                        particles += block_squares
        self.particles += particles

    def update_particles(self) -> None:
        """Updates particles and removes particles too small to render"""
        for particle in self.particles:
            if type(particle) is Circle or type(particle) is Blood:
                particle.update_position()
                particle.decrease_size(0.10)
                if particle.update_existance() is False:
                    self.particles.remove(particle)
            elif type(particle) is Square or type(particle) is BlockSquare:
                particle.update_position()
                particle.decrease_size(decay=0.5)
                if particle.width <= 1:
                    self.particles.remove(particle)

    def print_particles_n(self):
        """Prints how many particles are currently active"""
        print(len(self.particles))

    def update_player(self) -> None:
        """Runs updates for the player"""
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
        """Generates list of objects to be sent for rendering"""
        layers = [
            self.current_level.layer0,
            self.current_level.layer1,
            self.current_level.layer2,
            self.current_level.layer3,
            self.current_level.layer4,
            self.current_level.layer5] + (
            self.current_level.objects +
            self.current_level.current_wave_enemies +
            [self.character] +
            self.particles +
            [self.current_level.layer6,
             self.current_level.layer7] +
            [ui.health_bar] +
            [ui.score]
            )
        return layers

    def update_player_frame(self) -> None:
        """Updates frames for player animations"""
        self.character.current_time = pygame.time.get_ticks()
        if self.character.current_time - self.character.last_update >= self.character.frame_rate:
            self.character.frame += 1
            self.character.last_update = self.character.current_time

    def update_enemies_frame(self) -> None:
        """Updates frames  for animations of all enemies"""
        for enemy in self.current_level.current_wave_enemies:
            if enemy.exist:
                current_time = pygame.time.get_ticks()
                if current_time - enemy.last_update >= enemy.frame_rate:
                    enemy.frame += 1
                    enemy.last_update = current_time
                enemy.reset_frames()

    def update_enemies_states(self) -> None:
        """Updates states of all active enemies"""
        for enemy in self.current_level.current_wave_enemies:
            enemy.update_states()

    def update_objects(self) -> None:
        """Updates attributes of objects and remove picked or destoryed ones"""
        for object in self.current_level.objects:
            object.get_picked(self.character)
            object.update()
            if object.exist is False:
                self.current_level.objects.remove(object)

    def update_enemies_existance(self, print_info=False) -> None:
        """Checks if enemy exists and runs on enemy death mechanics"""
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
                        self.current_level.generate_dropable_items(5, enemy)
                    if type(enemy) is enemies.Imp:
                        self.current_level.score += 30
                        self.current_level.generate_dropable_items(20, enemy)
                    self.current_level.current_wave_enemies.remove(enemy)
                    if print_info:
                        print(f"Enemy , {enemy}, removed from the active enemies list")

    def check_for_level_end(self) -> None:
        """Checks and controls level end condition"""
        if ((self.current_level.current_wave == self.current_level.total_waves
                and len(self.current_level.current_wave_enemies) < 1)
                or self.character.health == 0):
            self.in_game = False
            self.in_menu = True
            self.menu_manager.current_menu = menu.score_menu
            self.menu_manager.current_menu.name = "SCORE:" + str(self.current_level.score)
            self.menu_manager.current_menu.update_surface()

    def update_layer_scroll(self) -> None:
        """"Updates world objects position on the screen"""
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
        for object in self.current_level.objects:
            object.x += self.character.speed

    def update_camera(self) -> None:
        """Moves camera based on player facing direction"""
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
                for object in self.current_level.objects:
                    object.x -= 0.5
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
                for object in self.current_level.objects:
                    object.x += 0.5

    def update_setting_buttons(self) -> None:
        """Controls settings button labels"""
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
        """Returns on Hit sound object"""
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
    def get_hit_sound(object: player.Player | enemies.Enemy | enemies.Imp | enemies.Demon) -> sound.HitSound:
        """Returns on Hit sound object"""
        current_time = pygame.time.get_ticks()
        downtime_hit = object.hit_sound.DOWNTIME
        last_update_hit = object.hit_sound.last_update
        if current_time - last_update_hit > downtime_hit:
            object.hit_sound.last_update = current_time
            return object.hit_sound

    def get_attack_sounds(self) -> List[sound.HitSound]:
        """Returns on Hit sound objects"""
        attack_sounds = []
        for enemy in self.current_level.current_wave_enemies:
            if enemy.attacking:
                if enemy.attack.hit(enemy.frame, self.character.hitbox):
                    sound = Model.get_attack_sound(enemy)
                    hit_sound = Model.get_hit_sound(self.character)
                    if self.character.guarding:
                        attack_sounds.append(player_block_sound)
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

    def play_level_sounds(self) -> None:
        """Plays current level ambient sounds"""
        if self.current_level is not None:
            self.current_level.ambient_sound.play(loops=-1)

    def get_animation_sound(self) -> sound.AnimationSound:
        """Returns player animation sound object"""
        if self.character.attacking_normal:
            if self.character.frame == attack_normal_sound1.frame:
                return attack_normal_sound1
            if self.character.frame == attack_normal_sound2.frame:
                return attack_normal_sound2
        if self.character.attacking_upper:
            if self.character.frame == attack_upper_sound1.frame:
                return attack_upper_sound1

    def get_objects_sounds(self) -> List[sound.HitSound]:
        """Returns object picked sound or None"""
        sounds = []
        current_time = pygame.time.get_ticks()
        for obj in self.current_level.objects:
            if obj.picked:
                if current_time - obj.picked_sound.last_update > obj.picked_sound.DOWNTIME:
                    sounds.append(obj.picked_sound)
                obj.picked_sound.last_update = current_time
        return sounds

    def get_sounds(self) -> List[Union[sound.HitSound, sound.AnimationSound]]:
        """Returns list of currently active sound objects"""
        if len(self.sounds) > 200:
            self.sounds = self.sounds[:-30]
        sounds = []
        animation_sound = self.get_animation_sound()
        if animation_sound:
            sounds.append(animation_sound)
        hit_sounds = self.get_attack_sounds()
        sounds += hit_sounds
        sounds += self.get_objects_sounds()
        return sounds
