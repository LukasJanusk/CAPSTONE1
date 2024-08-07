import pygame
import math
import os
from typing import Union, List
from . import enemies
from . import player
from . import animations
from . import layer
from . import menu
from . import ui
from . import particles
from . import user


class View:
    font_small = pygame.font.Font(
        os.path.join(".", "assets", "fonts", "font.otf"), 18)
    font_medium = pygame.font.Font(
        os.path.join(".", "assets", "fonts", "font.otf"), 25)
    font_large = pygame.font.Font(
        os.path.join(".", "assets", "fonts", "font.otf"), 45)

    @staticmethod
    def render(
            screen: pygame.Surface,
            score: str,
            layers: List[
                Union[
                    animations.Animation,
                    enemies.Enemy,
                    enemies.Demon,
                    enemies.Imp,
                    layer.Layer,
                    player.Player,
                    particles.Circle,
                    ui.Healthbar,
                    ui.Score]] = [],
            draw_health_bars: bool = True,
            draw_hitboxes: bool = True
            ):
        for object in layers:
            if object is None:
                continue
            elif type(object) is layer.Layer:
                View.render_layer(screen, object)
            elif (type(object) is enemies.Enemy or
                  type(object) is enemies.Demon or
                  type(object) is enemies.Imp):
                View.render_enemy(screen, object)
                if draw_health_bars:
                    View.draw_enemy_health_bar(screen, object)
            elif type(object) is player.Player:
                View.render_player(screen, object)
            elif type(object) is ui.Healthbar:
                screen.blit(object.draw_health_bar(), (5, 5))
            elif type(object) is ui.Score:
                View.draw_score(screen, object, score)
            elif type(object) is particles.Circle:
                object.render_circle(screen)
            else:
                print("no object to render")
            if draw_hitboxes:
                player_object = [
                    item for item in layers if isinstance(item, player.Player)][0]
                enemies_objects = [
                    item for item in layers if isinstance(item, enemies.Demon | enemies.Imp)]
                View.draw_hitboxes(screen, player_object, enemies_objects)

    @staticmethod
    def draw_score(screen: pygame.Surface, object: ui.Score, score: str):
        score_surface = object.get_score_surface(score)
        x = View.center(screen, score_surface)
        screen.blit(score_surface, (x, 10))

    @staticmethod
    def render_layer(screen: pygame.Surface, layer: layer.Layer):
        screen_width = screen.get_width()
        tiles = math.ceil(screen_width/layer.width) + 1
        for i in range(tiles):
            screen.blit(layer._IMAGE, (i * layer.width + layer.distance, 0))
            screen.blit(layer._IMAGE, (-i * layer.width + layer.distance, 0))

    @staticmethod
    def render_enemy(screen: pygame.Surface, enemy: enemies.Demon | enemies.Imp):
        animation: animations.Animation = enemy.current_animation
        animation.animate(screen, enemy.frame, enemy.facing_right)

    @staticmethod
    def render_player(screen: pygame.Surface, player: player.Player):
        animation = View.get_fixed_position(player)
        animation.animate(screen, player.frame, player.facing_right)

    @staticmethod
    def draw_hitboxes(
            screen: pygame.Surface,
            player: player.Player,
            enemies: List[Union[enemies.Enemy, enemies.Demon, enemies.Imp]]
            ):
        View.draw_player_hitbox(screen, player)
        View.draw_enemies_hitboxes(screen, enemies)
        View.draw_player_attack_hitbox(screen, player)
        View.draw_enemies_attack_hitboxes(screen, enemies)

    @staticmethod
    def draw_player_hitbox(screen: pygame.Surface, player: player.Player):
        if player.hit:
            pygame.draw.rect(screen, (255, 0, 0), player.hitbox, 2)
        else:
            pygame.draw.rect(screen, (0, 255, 0), player.hitbox, 2)

    @staticmethod
    def draw_player_attack_hitbox(screen: pygame.Surface, player: player.Player):
        if player.current_attack is not None:
            player.current_attack.draw_hitbox(screen, player.frame)

    @staticmethod
    def draw_enemies_attack_hitboxes(screen: pygame.Surface, enemies: List[Union[
                    enemies.Enemy,
                    enemies.Demon,
                    enemies.Imp]]):
        for enemy in enemies:
            if enemy.attacking:
                enemy.attack.draw_hitbox(screen, enemy.frame)

    @staticmethod
    def draw_enemies_hitboxes(screen: pygame.Surface, enemies: List[enemies.Enemy]):
        for enemy in enemies:
            if enemy is not None:
                if enemy.hit:
                    pygame.draw.rect(screen, (255, 0, 0), enemy.hitbox, 2)
                else:
                    pygame.draw.rect(screen, (0, 255, 0), enemy.hitbox, 2)

    @staticmethod
    def draw_enemy_health_bar(screen: pygame.Surface, enemy: enemies.Demon | enemies.Imp):
        health_bar_bg = pygame.Surface((enemy.hitbox_width, 10))
        health_bar_width = int(enemy.hitbox_width * enemy.health / enemy.max_health)
        if health_bar_width < 0:
            health_bar_width = 0
        health_bar_bg.fill((0, 0, 0))
        health_bar = pygame.Surface((health_bar_width, 8))
        health_bar.fill((65, 155, 0))
        health_bar_bg.blit(health_bar, (0, 1))
        x = View.center(enemy.current_animation.animation_list[0], health_bar_bg)
        screen.blit(health_bar_bg, (enemy.x + x, enemy.y + 10))

    @staticmethod
    def center(screen: pygame.Surface, object: pygame.Surface) -> int:
        object_rect = object.get_rect()
        screen_rect = screen.get_rect()
        x = (screen_rect.width - object_rect.width) // 2
        return x

    @staticmethod
    def get_fixed_position(player: player.Player):
        if player.current_animation == player.IDLE_ANIMATION:
            player.IDLE_ANIMATION.x = player.x
            player.IDLE_ANIMATION.y = player.y
            player.IDLE_ANIMATION.buffer_facing_left_x = -24
            return player.IDLE_ANIMATION
        elif player.current_animation == player.WALKING_ANIMATION:
            player.WALKING_ANIMATION.x = player.x
            player.WALKING_ANIMATION.y = player.y - 15
            player.WALKING_ANIMATION.buffer_facing_left_x = -15
            return player.WALKING_ANIMATION
        elif player.current_animation == player.ATTACK_NORMAL_ANIMATION:
            player.ATTACK_NORMAL_ANIMATION.x = player.x - 10
            player.ATTACK_NORMAL_ANIMATION.y = player.y - 8
            player.ATTACK_NORMAL_ANIMATION.buffer_facing_left_x = -55
            return player.ATTACK_NORMAL_ANIMATION
        elif player.current_animation == player.ATTACK_UPPER_ANIMATION:
            player.ATTACK_UPPER_ANIMATION.x = player.x - 90
            player.ATTACK_UPPER_ANIMATION.y = player.y - 40
            return player.ATTACK_UPPER_ANIMATION
        elif player.current_animation == player.JUMPING_ANIMATION:
            player.JUMPING_ANIMATION.x = player.x
            player.JUMPING_ANIMATION.y = player.y
            player.JUMPING_ANIMATION.buffer_facing_left_x = -15
            return player.JUMPING_ANIMATION
        elif player.current_animation == player.GUARD_ANIMATION:
            player.GUARD_ANIMATION.x = player.x
            player.GUARD_ANIMATION.y = player.y
            player.GUARD_ANIMATION.buffer_facing_left_x = -20
            return player.GUARD_ANIMATION

    @staticmethod
    def draw_menus(screen: pygame.Surface, current_menu: menu.Menu, user: user.User):
        screen.fill(current_menu.colour)
        current_menu.center_text(screen)
        screen.blit(current_menu.text_surface, (current_menu.text_x, 30))
        if current_menu is menu.high_scores_menu:
            current_menu.selected_button.y = 550
            current_menu.selected_button.center_button(screen)
            View.draw_highscores(screen, user)
            screen.blit(
                current_menu.selected_button.surface,
                (current_menu.selected_button.x, current_menu.selected_button.y)
                )
        else:
            for index, button in enumerate(current_menu.buttons):
                button.center_button(screen)
                screen.blit(button.surface, (button.x, 150 + index * 50))

    @classmethod
    def draw_fps(cls, screen: pygame.Surface, fps: int):
        screen_rect = screen.get_rect()
        fps_surface = cls.font_small. render(f"FPS: {fps}", True, (255, 255, 255))
        fps_surface.get_width()
        x = screen_rect.width - (fps_surface.get_width() + 10)
        screen.blit(fps_surface, (x, 10))

    @classmethod
    def draw_wave_number(
            cls,
            screen: pygame.Surface,
            total_waves: int,
            current_wave: int,
            coordinates: tuple = (10, 30),
            scale: float = None
            ):
        text_surface = cls.font_medium.render(f"Wave: {current_wave}/{total_waves}", True, (255, 255, 255))
        if scale:
            text_surface = pygame.transform.smoothscale(text_surface, (scale, scale))
        screen.blit(text_surface, coordinates)

    @classmethod
    def draw_highscores(cls, screen: pygame.Surface, user: user.User):
        bg_rect = pygame.rect.Rect(0, 0, 500, 400)
        bg = pygame.surface.Surface((500, 400))
        bg.fill((28, 73, 98))
        x = View.center(screen, bg)
        bg_rect.x = x
        bg_rect.y = 130
        scores = [
            cls.font_large.render(
                "LEVEL 1: " + str(user.level1_highscore),
                True,
                (0, 0, 0)),
            cls.font_large.render(
                "LEVEL 2: " + str(user.level2_highscore),
                True,
                (0, 0, 0)),
            cls.font_large.render(
                "LEVEL 3: " + str(user.level3_highscore),
                True,
                (0, 0, 0)),
            cls.font_large.render(
                "LEVEL 4: " + str(user.level4_highscore),
                True,
                (0, 0, 0)),
            cls.font_large.render(
                "LEVEL 5: " + str(user.level5_highscore),
                True,
                (0, 0, 0))
                ]
        for index, score in enumerate(scores):
            bg.blit(score, (20, 20 + 50 * index))
        screen.blit(bg, bg_rect)
