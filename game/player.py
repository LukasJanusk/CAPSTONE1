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
    current_time = None
    health: float = 1000
    speed: float = 1.5
    jump_strength: float = 16
    vertical_position: float = 0
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
    current_animation = None

    def __post_init__(self):
        self.IDLE_ANIMATION = animations.Animation(spritesheets.idle_animation_list, self.x, self.y, -24)
        self.WALKING_ANIMATION = animations.Animation(spritesheets.walking_animation_list, self.x, self.y - 15, -15)
        self.GUARD_ANIMATION = animations.Animation(spritesheets.guard_animation_list, self.x, self.y, -20)
        self.JUMPING_ANIMATION = animations.Animation(spritesheets.jumping_animation_list, self.x, self.y, -15)
        self.ATTACK_UPPER_ANIMATION = animations.Animation(spritesheets.attack_upper_list, self.x - 90, self.y - 40)
        self.ATTACK_NORMAL_ANIMATION = animations.Animation(spritesheets.attack_normal_list, self.x - 10, self.y - 8, -55)
        if self.current_animation is None:
            self.current_animation is self.IDLE_ANIMATION

    def reset_frames(self):
        if self.attacking_upper:
            if self.frame > 14:
                self.frame = 0
        if self.attacking_normal:
            if self.frame > 6:
                self.frame = 0
        if self.guarding:
            if self.frame > 3:
                self.frame = 0
        if self.jumping:
            if self.frame >= 4:
                self.frame = 0
        if self.running:
            if self.frame == 6:
                self.frame = 0
        if self.walking:
            if self.frame > 5:
                self.frame = 0
        if self.idle:
            if self.frame > 7:
                self.frame = 0

    def update_jumping(self):
        if self.jumping:
            self.y = self.y - self.jump_strength + self.vertical_position
            self.vertical_position += 0.5
            if self.y >= 400:
                self.jumping = False
                self.vertical_position = 0
                # self.idle = True
            # if self.vertical_position == 0:
            #     self.y = 400
            # if self.y > 400:
            #     self.vertical_position = 0
            #     self.jumping = False

    def update_speed(self):
        if not self.jumping:
            self.aerial_movement = False
        self.speed = 0
        if self.running is True:
            self.speed += 2.5
        if self.walking is True:
            self.speed += 1.5
        if self.dashing:
            self.speed += 4
        if self.attack_moving is True:
            self.speed += 0.4
        if self.aerial_movement is True:
            self.speed += 2
        if self.ducking is True:
            self.speed = 0
        if self.guarding is True:
            self.speed = 0
        if self.idle is True:
            self.speed = 0
        if self.facing_right:
            self.speed = self.speed * -1

    def get_current_animation(self):
        if self.attacking_normal:
            self.current_animation = self.ATTACK_NORMAL_ANIMATION
        elif self.attacking_upper:
            self.current_animation = self.ATTACK_UPPER_ANIMATION
        elif self.running:
            self.current_animation = self.WALKING_ANIMATION
        elif self.walking:
            self.current_animation = self.WALKING_ANIMATION
        elif self.jumping:
            self.current_animation = self.JUMPING_ANIMATION
        elif self.guarding:
            self.current_animation = self.GUARD_ANIMATION
        else:
            self.current_animation = self.IDLE_ANIMATION


char = Player(100, 400, 1)
