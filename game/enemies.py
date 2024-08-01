import pygame
import animations
import spritesheets
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
# from typing import Optional


class BaseEnemy(ABC):
    @abstractmethod
    def update_frames(self):
        pass

    def update_states(self):
        pass


@dataclass
class Enemy(BaseEnemy):
    NAME: str
    x: int
    y: int
    hitbox_width: float
    hitbox_height: float
    health: float = 100
    damage: int = 0
    scale: float = 1
    frame: int = 0
    frame_rate: int = 160
    last_update: float = field(default_factory=lambda: pygame.time.get_ticks())
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

    def __post_init__(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.hitbox_width, self.hitbox_height)


@dataclass
class Demon(Enemy):
    AI = None
    health: float = 10000
    damage: int = 50
    sprite_sheet_list = spritesheets.demon_animations
    attack_animation = None
    hit_animation = None
    death_animation = None
    running_animation = None
    idle_animation = None

    def __post_init__(self):
        super().__post_init__()
        self.attack_animation = animations.Animation(self.x, self.y, self.sprite_sheet_lsit[3], 0, 0, (150, 150, 150))
        self.hit_animation = animations.Animation(self.x, self.y, self.sprite_sheet_lsit[1], 0, 0, (150, 150, 150))
        self.death_animation = animations.Animation(self.x, self.y, self.sprite_sheet_lsit[2], 0, 0, (150, 150, 150))
        self.running_animation = animations.Animation(self.x, self.y, self.sprite_sheet_lsit[4], 0, 0, (150, 150, 150))
        self.idle_animation = animations.Animation(self.x, self.y, self.sprite_sheet_lsit[0], 0, 0, (150, 150, 150))
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