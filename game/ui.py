import os
import pygame
from dataclasses import dataclass
from math import ceil
from . import player
from .spritesheets import SpriteSheets
from abc import ABC, abstractmethod

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


@dataclass
class Bar(ABC):
    x: int
    y: int
    character = player.char
    bar_surface: pygame.surface.Surface = None
    value: int = 0
    max_value: int = 0
    capacity: int = 0
    bar_bg_surface: pygame.surface.Surface = None
    colour = (255, 255, 255)
    bg_colour = (0, 0, 0)

    @abstractmethod
    def get_values(self) -> bool:
        """Checks if values changed and returns bool as a result"""
        pass

    def draw_bar(self, screen: pygame.surface.Surface):
        if self.get_values():
            return self.bar_bg_surface
        else:
            screen_width = screen.get_width()
            value_width = int(self.value * 0.3)
            self.x = screen_width - self.max_value
            text = font.render(
                f"{ceil(self.value)}/{self.capacity}", True, (255, 255, 255))
            if self.value < 0:
                self.value = 0
            bar_bg = pygame.Surface((self.max_value, 22))
            bar = pygame.Surface((value_width, 20))
            bar_bg.fill(self.bg_colour)
            bar.fill(self.colour)
            bar_bg.blit(bar, (self.max_value - value_width, 1))
            bar_bg.blit(text, (115, 1))
            self.bar_bg_surface = bar_bg
            return self.bar_bg_surface


@dataclass
class Fire(Bar):

    def __post_init__(self):
        self.capacity = self.character.maximum_fire
        self.colour = (225, 90, 20)
        self.value = int(self.character.fire * 0.3)
        self.max_value = int(self.character.maximum_fire * 0.3 + 2)
        self.bar_surface = pygame.surface.Surface((self.character.fire, 20))
        self.bar_bg_surface = pygame.surface.Surface((self.max_value, 22))
        self.bar_surface.fill(self.colour)
        self.bar_bg_surface.fill(self.bg_colour)
        self.bar_bg_surface.blit(self.bar_surface, (1, 1))

    def get_values(self) -> bool:
        self.capacity = self.character.maximum_fire
        if self.value == self.character.fire:
            return True
        else:
            self.value = self.character.fire
            return False


@dataclass
class Cold(Bar):

    def __post_init__(self):
        self.capacity = self.character.maximum_cold
        self.colour = (163, 235, 240)
        self.value = int(self.character.cold * 0.3)
        self.max_value = int(self.character.maximum_cold * 0.3 + 2)
        self.bar_surface = pygame.surface.Surface((self.character.cold, 20))
        self.bar_bg_surface = pygame.surface.Surface((self.max_value, 22))
        self.bar_surface.fill(self.colour)
        self.bar_bg_surface.fill(self.bg_colour)
        self.bar_bg_surface.blit(self.bar_surface, (1, 1))

    def get_values(self) -> bool:
        self.capacity = self.character.maximum_cold
        if self.value == self.character.cold:
            return True
        else:
            self.value = self.character.cold
            return False


@dataclass
class Lightning(Bar):

    def __post_init__(self):
        self.capacity = self.character.maximum_lightning
        self.colour = (48, 55, 244)
        self.value = int(self.character.lightning * 0.3)
        self.max_value = int(self.character.maximum_lightning * 0.3 + 2)
        self.bar_surface = pygame.surface.Surface((self.character.lightning, 20))
        self.bar_bg_surface = pygame.surface.Surface((self.max_value, 22))
        self.bar_surface.fill(self.colour)
        self.bar_bg_surface.fill(self.bg_colour)
        self.bar_bg_surface.blit(self.bar_surface, (1, 1))

    def get_values(self) -> bool:
        self.capacity = self.character.maximum_lightning
        if self.value == self.character.lightning:
            return True
        else:
            self.value = self.character.lightning
            return False


fire_bar = Fire(498, 5)
cold_bar = Cold(498, 35)
lightning_bar = Lightning(498, 65)
health_bar = Healthbar()
score = Score()
