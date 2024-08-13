import pygame
from dataclasses import dataclass
from . import player
from . import animations
from . import sound


@dataclass
class Object:
    x: int
    y: int


@dataclass
class Breakable(Object):
    hitbox: pygame.rect.Rect
    health: int
    idle: bool = True
    hit: bool = False
    dead: bool = False
    idle_animation: animations.Animation = None
    hit_animation: animations.Animation = None
    dead_animation: animations.Animation = None
    current_animation: animations.Animation = None
    hit_sound: sound.HitSound = None
    last_update = pygame.time.get_ticks()
    frame_time: int = 160


@dataclass
class Pickable(Object):
    width: int
    height: int
    hitbox: pygame.rect.Rect
    idle: bool = True
    picked: bool = False
    idle_animation: animations.Animation = None
    picked_animation: animations.Animation = None
    current_animation: animations.Animation = None
    picked_sound: sound.HitSound = None
    last_update = pygame.time.get_ticks()
    frame_time: int = 160
    _frame: int = 0

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value > (len(self.current_animation.animation_list) - 1):
            self.frame = 0


@dataclass
class Health_Potion(Pickable):
    value: int = 50
    width: int = 50
    height: int = 50

    def __post_init__(self):
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def get_picked(self, player: player.Player):
        if self.rect.colliderect(player.hitbox):
            player.health += self.value
