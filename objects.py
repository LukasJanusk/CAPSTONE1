import pygame
from dataclasses import dataclass


@dataclass
class Object:
    x: int
    y: int


@dataclass
class Breakable(Object):
    hitbox: pygame.rect.Rect
    health: int
    idle = True
    hit = False
    dead = False
    idle_animation = None
    hit_animation = None
    dead_animation = None
    hit_sound = None


@dataclass
class Pickable(Object):
    hitbox: pygame.rect.Rect
    idle = True
    picked = False
    idle_animation = None
    picked_animation = None
    picked_sound = None
