import os
import pygame
from dataclasses import dataclass
from math import ceil
from . import player
from .spritesheets import SpriteSheets

pygame.init()
screen = pygame.display.set_mode((800, 640))
font = pygame.font.Font(os.path.join(".", "assets", "fonts", "font.otf"), 18)


@dataclass
class UI(SpriteSheets):
    _IMAGE: pygame.Surface = None
    x: int = 0
    y: int = 0
    frame: int = 0

    def __post_init__(self):
        self.width = self.sheet.get_width()
        self.height = self.sheet.get_height()
        self._IMAGE = self.get_image(self.frame, self.width, self.height, 1, (150, 150, 150))


@dataclass
class Healthbar:
    character = player.char
    health_bar_surface: pygame.Surface = None
    health: int = 0

    def __post_init__(self):
        self.health_bar_surface = self.draw_health_bar()
        self.health = self.character.health

    @property
    def get_health_bar_surface(self):
        return self.health_bar_surface

    @get_health_bar_surface.setter
    def get_health_bar_surface(self, value):
        if self.character.health != self.health:
            self.health_bar_surface = self.draw_health_bar()

    def draw_health_bar(self):
        if self.character.health == self.health:
            return self.health_bar_surface
        text = font.render(f"{ceil(self.character.health)}/1000", True, (255, 255, 255))
        full_health_width = 302
        current_health_width = int(self.character.health * 0.3)
        if current_health_width < 0:
            current_health_width = 0
        if current_health_width < 80:
            colour = (160, 15, 15)
        else:
            colour = (65, 155, 0)
        health_bar_bg = pygame.Surface((full_health_width, 26))
        health_bar = pygame.Surface((current_health_width, 24))
        health_bar_bg.fill((0, 0, 0))
        health_bar.fill(colour)
        health_bar_bg.blit(health_bar, (1, 1))
        health_bar_bg.blit(text, (115, 1))
        self.health_bar_surface = health_bar_bg
        self.health = self.character.health
        return self.health_bar_surface


health_bar = Healthbar()
