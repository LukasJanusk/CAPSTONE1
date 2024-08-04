import pygame
from dataclasses import dataclass
from abc import ABC, abstractmethod
from . import attacks
from . import animations
from . import spritesheets
# from typing import Optional


class BaseEnemy(ABC):
    @abstractmethod
    def reset_frames(self):
        pass

    def update_states(self):
        pass

    def update_hitbox(self):
        pass


@dataclass
class Enemy(BaseEnemy):
    x: int
    y: int
    hitbox_width: int = 50
    hitbox_height: int = 50
    health: float = 100
    max_health: float = 100
    damage: int = 0
    scale: float = 1
    _frame: int = 0
    _frame_rate: int = 160
    last_update = pygame.time.get_ticks()
    stun_duration: int = 200
    speed: float = 1.5
    facing_right: bool = False
    running: bool = False
    attacking: bool = True
    guarding: bool = False
    stunned: bool = False
    hit: bool = False
    idle: bool = True
    dead: bool = False
    exist: bool = True
    hitbox = None
    current_animation = None
    attack = None

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if type(value) is not int:
            raise TypeError("Wrong type for value: frame")
        if value < 0:
            self._frame = 0
        if len(self.current_animation.animation_list) - 1 < value:
            self._frame = 0
        else:
            self._frame = value

    @property
    def frame_rate(self):
        return self._frame_rate


@dataclass
class Demon(Enemy):
    AI = None
    health: float = 10000
    max_health: float = 10000
    damage: int = 50
    sprite_sheet_list = spritesheets.demon_animations
    attack_animation = None
    hit_animation = None
    death_animation = None
    running_animation = None
    idle_animation = None
    hitbox_height = 420
    hitbox_width = 300
    weight = 10
    hitbox = None

    def __post_init__(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.hitbox_width, self.hitbox_height)
        self.idle_animation = animations.Animation(self.sprite_sheet_list[0], self.x, self.y, 0, 0, (150, 150, 150))
        self.hit_animation = animations.Animation(self.sprite_sheet_list[1], self.x, self.y, 0, 0, (150, 150, 150))
        self.death_animation = animations.Animation(self.sprite_sheet_list[2], self.x, self.y, 0, 0, (150, 150, 150))
        self.attack_animation = animations.Animation(self.sprite_sheet_list[3], self.x, self.y, 0, 0, (150, 150, 150))
        self.running_animation = animations.Animation(self.sprite_sheet_list[4], self.x, self.y, 0, 0, (150, 150, 150))
        self.attack = attacks.Attack(self.damage, [6], 300, 180, 120, 270, -40, 0)
        if self.current_animation is None:
            self.current_animation = self.idle_animation

    def reset_frames(self):
        if self.exist:
            if self.dead:
                if self.frame >= 6:
                    self.exist = False
                    self.y = -500
            elif self.hit is True:
                if self.frame >= 5:
                    self.frame = 0
            elif self.attacking is True:
                if self.frame >= 8:
                    self.frame = 0
                    self.attacking = False
            elif self.running is True:
                if self.frame >= 4:
                    self.frame = 0
            elif self.idle is True:
                if self.frame >= 4:
                    self.frame = 0
        return self.frame

    def update_states(self):
        if self.exist:
            if self.dead:
                self.idle = False
                self.attacking = False
                self.hit = False
                self.current_animation = self.death_animation
            elif self.hit:
                self.idle = False
                self.attacking = False
                self.running = False
                self.current_animation = self.hit_animation
                if self.frame == 4:
                    self.hit = False
                    self.frame = 0
                    self.idle = True
                    self.current_animation = self.idle_animation
            elif self.running:
                self.idle = False
                self.attacking = False
                self.current_animation = self.running_animation
            elif self.attacking:
                self.idle = False
                self.running = False
                self.current_animation = self.attack_animation
            elif self.idle:
                self.hit = False
                self.current_animation = self.idle_animation

    def update_hitbox(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.hitbox_width, self.hitbox_height)


@dataclass
class Imp(Enemy):
    AI = None
    health: float = 1000
    max_health: float = 1000
    damage: int = 5
    sprite_sheet_list = spritesheets.imp_animations
    attack_animation = None
    hit_animation = None
    death_animation = None
    running_animation = None
    idle_animation = None
    hitbox_height = 120
    hitbox_width = 60
    weight = 80
    hitbox = None

    def __post_init__(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.hitbox_width, self.hitbox_height)
        self.idle_animation = animations.Animation(self.sprite_sheet_list[0], self.x, self.y, 0, 0, (150, 150, 150))
        self.hit_animation = animations.Animation(self.sprite_sheet_list[1], self.x, self.y, 0, 0, (150, 150, 150))
        self.death_animation = animations.Animation(self.sprite_sheet_list[2], self.x, self.y, 0, 0, (150, 150, 150))
        self.attack_animation = animations.Animation(self.sprite_sheet_list[3], self.x, self.y, 0, 0, (150, 150, 150))
        self.running_animation = animations.Animation(self.sprite_sheet_list[4], self.x, self.y, 0, 0, (150, 150, 150))
        self.attack = attacks.Attack(self.damage, [1, 2], 50, 30, 130, 75, -30, 0)
        if self.current_animation is None:
            self.current_animation = self.idle_animation

    def reset_frames(self):
        if self.exist:
            if self.dead:
                if self.frame >= 6:
                    self.exist = False
                    self.y = -500
            elif self.hit is True:
                if self.frame > 6:
                    self.frame = 0
            elif self.attacking is True:
                if self.frame > 4:
                    self.frame = 0
                    self.attacking = False
            elif self.running is True:
                if self.frame > 4:
                    self.frame = 0
            elif self.idle is True:
                if self.frame > 4:
                    self.frame = 0
        return self.frame

    def update_states(self):
        if self.exist:
            if self.dead:
                self.idle = False
                self.attacking = False
                self.hit = False
                self.current_animation = self.death_animation
            elif self.hit:
                self.idle = False
                self.attacking = False
                self.running = False
                self.current_animation = self.hit_animation
                if self.frame == 6:
                    self.hit = False
                    self.frame = 0
                    self.idle = True
                    self.current_animation = self.idle_animation
            elif self.running:
                self.idle = False
                self.attacking = False
                self.current_animation = self.running_animation
            elif self.attacking:
                self.idle = False
                self.running = False
                self.current_animation = self.attack_animation
            elif self.idle:
                self.hit = False
                self.current_animation = self.idle_animation

    def update_hitbox(self):
        self.hitbox = pygame.Rect(self.x + 50, self.y, self.hitbox_width, self.hitbox_height)
