import pygame
import enemies
import player
import animations
import layer
import math
from typing import Union, List


class View:
    @classmethod
    def render(cls, screen: pygame.Surface, layers: List[Union[animations.Animation, enemies.Enemy, layer.Layer]] = []):
        for object in layers:
            if object is None:
                continue
            elif type(object) is layer.Layer:
                View.render_layer(screen, object)
            elif type(object) is enemies.Enemy:
                View.render_enemy(screen, object)
            elif type(object) is player.Player:
                View.render_player(screen, object)
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
        animation: animations.Animation = player.current_animation
        animation.x = player.x
        animation.y = player.y
        animation.animate(screen, player.frame, player.facing_right)
