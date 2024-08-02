import pygame
import enemies
import player
import animations
import layer
import math
from typing import Union, List


class View:
    @classmethod
    def render(cls,
               screen: pygame.Surface,
               layers: List[Union[animations.Animation, enemies.Enemy, layer.Layer, player.Player]] = [],
               draw_health_bars: bool = False
               ):
        for object in layers:
            if object is None:
                continue
            elif type(object) is layer.Layer:
                View.render_layer(screen, object)
            elif type(object) is enemies.Enemy:
                View.render_enemy(screen, object)
                if draw_health_bars:
                    View.draw_enemy_health_bar(screen, object)
            elif type(object) is player.Player:
                View.render_player(screen, object)
            elif type(object) is pygame.Surface:
                screen.blit(object, (0, 0))
            else:
                print("no object to render")
            # elif layer_object is effects.Particle:
            #   pass

    @classmethod
    def render_layer(cls, screen: pygame.Surface, layer: layer.Layer):
        screen_width = screen.get_width()
        tiles = math.ceil(screen_width/layer.width) + 1
        for i in range(tiles):
            screen.blit(layer._IMAGE, (i * layer.width + layer.distance, 0))
            screen.blit(layer._IMAGE, (-i * layer.width + layer.distance, 0))

    @classmethod
    def render_enemy(cls, screen: pygame.Surface, enemy: enemies.Enemy):
        animation: animations.Animation = enemy.current_animation
        animation.animate(screen, enemy.frame, enemy.facing_right)

    @classmethod
    def render_player(cls, screen: pygame.Surface, player: player.Player):
        animation = View.get_fixed_position(player)
        animation.animate(screen, player.frame, player.facing_right)

    @classmethod
    def draw_player_hitbox(cls, screen: pygame.Surface, player: player.Player):
        if player.hit:
            pygame.draw.rect(screen, (255, 0, 0), player.hitbox, 2)
        else:
            pygame.draw.rect(screen, (0, 255, 0), player.hitbox, 2)

    @classmethod
    def draw_player_attack_hitbox(cls, screen: pygame.Surface, player: player.Player):
        if player.current_attack is not None:
            player.current_attack.draw_hitbox(screen, player.frame)

    @classmethod
    def draw_enemies_hitboxes(cls, screen: pygame.Surface, enemies: List[enemies.Enemy]):
        for enemy in enemies:
            if enemy is not None:
                if enemy.hit:
                    pygame.draw.rect(screen, (255, 0, 0), enemy.hitbox, 2)
                else:
                    pygame.draw.rect(screen, (0, 255, 0), enemy.hitbox, 2)

    @classmethod
    def draw_enemy_health_bar(cls, screen: pygame.Surface, enemy: enemies.Enemy):
        health_bar_bg = pygame.Surface((enemy.hitbox_width, 10))
        health_bar_width = int(enemy.hitbox_width * enemy.health / enemy.max_health)
        health_bar_bg.fill((0, 0, 0))
        health_bar = pygame.Surface(health_bar_width, 8)
        health_bar.fill(65, 155, 0)
        health_bar.blit(health_bar_bg, (0, 1))
        x = View.center(enemy.current_animation.animation_list[0], health_bar_bg)
        screen.blit(health_bar_bg, (x, enemy.y + 10))

    @classmethod
    def center(cls, screen: pygame.Surface, object: pygame.Surface):
        object_rect = object.get_rect()
        screen_rect = screen.get_rect()
        x = (screen_rect.width - object_rect.width) // 2
        return x

    @classmethod
    def get_fixed_position(cls, player: player.Player):
        if player.current_animation == player.IDLE_ANIMATION:
            player.IDLE_ANIMATION.x = player.x
            player.IDLE_ANIMATION.y = player.y
            player.IDLE_ANIMATION.buffer_facing_left_x = -24
            return player.IDLE_ANIMATION
        elif player.current_animation == player.WALKING_ANIMATION:
            player.WALKING_ANIMATION.x = player.x
            player.WALKING_ANIMATION.y = player.y - 15
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
