import pygame
import animations
import spritesheets
from dataclasses import dataclass


@dataclass
class Player:
    x: int
    y: int
    scale: float = 1
    frame: int = 0
    frame_rate: int = 80
    last_update = pygame.time.get_ticks()
    health: float = 1000
    speed: float = 1.5
    jump_strength: float = 16
    hit:  bool = False
    idle: bool = True
    facing_right: bool = True
    walking: bool = False
    running: bool = False
    jump: bool = False
    jumping: bool = False
    guarding: bool = False
    ducking: bool = False
    attacking_upper: bool = False
    attacking_normal: bool = False
    dashing_right: bool = False
    dashing_left: bool = False
    dashing: bool = False
    attack_moving: bool = False
    aerial_movement: bool = False
    floating: bool = False
    falling: bool = False
    fire1: bool = False
    fire2: bool = False
    fire3: bool = True
    lightning1: bool = False
    lightning2: bool = False
    lightning3: bool = False
    ice1: bool = False
    ice2: bool = False
    ice3: bool = False
    IDLE_ANIMATION = None
    WALKING_ANIMATION = None
    GUARD_ANIMATION = None
    JUMPING_ANIMATION = None
    ATTACK_UPPER_ANIMATION = None
    ATTACK_NORMAL_ANIMATION = None

    def __post_init__(self):
        self.IDLE_ANIMATION = animations.Animation(self.x, self.y, spritesheets.idle_animation_list, -24, 0, (150, 150, 150))
        self.WALKING_ANIMATION = animations.Animation(self.x, self.y - 15, spritesheets.walking_animation_list, -15, 0, (150, 150, 150))
        self.GUARD_ANIMATION = animations.Animation(self.x, self.y, spritesheets.guard_animation_list, -20, 0, (150, 150, 150))
        self.JUMPING_ANIMATION = animations.Animation(self.x, self.y, spritesheets.jumping_animation_list, -15, 0, (150, 150, 150))
        self.ATTACK_UPPER_ANIMATION = animations.Animation(self.x - 90, self.y - 40, spritesheets.attack_upper_list, 0, 0, (150, 150, 150))
        self.ATTACK_NORMAL_ANIMATION = animations.Animation(self.x - 10, self.y - 8, spritesheets.attack_normal_list, -55, 0, (150, 150, 150))


char = Player(100, 300, 1)
