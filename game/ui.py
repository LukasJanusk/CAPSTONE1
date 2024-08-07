import os
import pygame
from dataclasses import dataclass
from math import ceil
from . import player
from .spritesheets import SpriteSheets

pygame.init()
screen = pygame.display.set_mode((800, 640))
font = pygame.font.Font(
    os.path.join(".", "assets", "fonts", "font.otf"),
    18)


@dataclass
class UI(SpriteSheets):
    _IMAGE: pygame.Surface = None
    x: int = 0
    y: int = 0
    frame: int = 0
    change: bool = False

    def __post_init__(self):
        self.width = self.sheet.get_width()
        self.height = self.sheet.get_height()
        self._IMAGE = self.get_image(
            self.frame, self.width, self.height, 1, (150, 150, 150))


@dataclass
class Score:
    last_update: int = pygame.time.get_ticks()
    width: int = 1
    height: int = 1
    _font = pygame.font.Font(
        os.path.join(".", "assets", "fonts", "font.otf"), 50)
    _font_size = 50
    rect: pygame.Rect = None
    surface: pygame.Surface = None

    @property
    def font(self):
        return pygame.font.Font(
            os.path.join(".", "assets", "fonts", "font.otf"), self.font_size)

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value: int):
        while value > 80:
            value -= 1
        while value < 40:
            value += 1
        self._font_size = value

    def get_score_surface(self, score: str):
        self.surface = self.font.render(score, True, (255, 255, 255))
        self.rect = self.surface.get_rect()
        return self.surface


@dataclass
class Healthbar:
    character = player.char
    _health_bar_surface: pygame.Surface = None
    health: int = 0

    def __post_init__(self):
        self.health_bar_surface = self.draw_health_bar()
        self.health = self.character.health

    @property
    def health_bar_surface(self):
        return self._health_bar_surface

    @health_bar_surface.setter
    def health_bar_surface(self, value):
        # Update later
        self._health_bar_surface = value

    @health_bar_surface.setter
    def get_health_bar_surface(self, value):
        if self.character.health != self.health:
            self.health_bar_surface = self.draw_health_bar()

    def draw_health_bar(self):
        if self.character.health == self.health:
            return self.health_bar_surface
        text = font.render(
            f"{ceil(self.character.health)}/1000", True, (255, 255, 255))
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
score = Score()
