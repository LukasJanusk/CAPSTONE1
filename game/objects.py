import pygame
from dataclasses import dataclass
import os
from . import player
from . import animations
from . import sound
from . import spritesheets


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
    hitbox: pygame.rect.Rect = None
    idle: bool = True
    picked: bool = False
    exist: bool = True
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
            self._frame = 0
        else:
            self._frame = value


@dataclass
class Health_Potion(Pickable):
    value: int = 50
    width: int = 50
    height: int = 50

    def __post_init__(self):
        self.hitbox = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.idle_animation = animations.Animation(spritesheets.health_potion_idle_animation_list, self.x, self.y, 0, 0, (150, 150, 150))
        self.picked_animation = animations.Animation(spritesheets.health_potion_picked_animation_list, self.x, self.y, 0, 0, (150, 150, 150))
        self.current_animation = self.idle_animation
        self.last_update = pygame.time.get_ticks()
        self.picked_sound = sound.HitSound(os.path.join(".", "assets", "sounds", "health_potion_picked_sound.ogg"), 334)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_time:
            self.frame += 1
            self.last_update = current_time
        self.idle_animation.x = self.x
        self.idle_animation.y = self.y
        self.picked_animation.x = self.x
        self.picked_animation.y = self.y
        self.hitbox = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        if self.picked:
            if self.frame == len(self.picked_animation.animation_list) - 1:
                self.exist = False

    def get_picked(self, player: player.Player) -> bool:
        if self.hitbox.colliderect(player.hitbox):
            if not self.picked:
                player.health += self.value
                self.picked = True
                self.current_animation = self.picked_animation
                return True
        return False
