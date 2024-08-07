import pygame
from dataclasses import dataclass
from typing import List
from .sound import HitSound


@dataclass
class Attack:
    sound: HitSound
    damage: int
    damage_frames: List[int]
    hitbox_width: int
    hitbox_height: int
    buffer_x: int = 0
    buffer_y: int = 0
    buffer_facing_left_x: int = 0
    buffer_facing_left_y: int = 0
    hitbox: pygame.Rect = None
    collision: bool = False

    def __post_init__(self):
        self.hitbox = pygame.Rect(
            self.buffer_x,
            self.buffer_y,
            self.hitbox_width,
            self.hitbox_height
            )

    def update_hitbox(self, x, y, facing_right):
        if facing_right:
            self.hitbox = pygame.Rect(
                self.buffer_x + x,
                self.buffer_y + y,
                self.hitbox_width,
                self.hitbox_height
                )
            return self.hitbox
        else:
            self.hitbox = pygame.Rect(
                (self.buffer_x + x + self.buffer_facing_left_x),
                (self.buffer_y + y + self.buffer_facing_left_y),
                (self.hitbox_width),
                (self.hitbox_height)
                )
            return self.hitbox

    def hit(self, attack_frame: int, enemy_hitbox: pygame.Rect):
        if attack_frame in self.damage_frames:
            if self.hitbox.colliderect(enemy_hitbox):
                self.collision = True
                return int(
                    self.damage * (self.damage_frames.index(attack_frame) / 5 + 1)
                    )
            else:
                return False
        else:
            self.collision = False
            return False

    def draw_hitbox(self, game_surface, frame):
        if frame in self.damage_frames:
            if self.collision:
                pygame.draw.rect(game_surface, (255, 0, 0), self.hitbox, 2)
            else:
                pygame.draw.rect(game_surface, (0, 0, 255), self.hitbox, 2)
