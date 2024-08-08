import pygame
import os
from dataclasses import dataclass
from typing import List, Union
from . import animations
pygame.mixer.init()


class AttackSound(pygame.mixer.Sound):
    def __init__(self, file, downtime):
        super().__init__(file)
        self.DOWNTIME: int = downtime
        self._last_update = pygame.time.get_ticks()

    @property
    def last_update(self):
        return self._last_update

    @last_update.setter
    def last_update(self, value: int):
        if value - self._last_update > self.DOWNTIME:
            self._last_update = value


@dataclass
class AnimationSound(pygame.mixer.Sound):
    start_frame: int
    end_frame: int
    downtime: int
    last_update = pygame.time.get_ticks()
    duration: int


class Sound_Controller:
    @staticmethod
    def play_sounds(
        objects: List[Union[
            AttackSound,
            AnimationSound,
           ]]):
        if objects is not None or objects != []:
            print(objects)
            for object in objects:
                if type(object) is animations.Animation:
                    pass
                elif type(object) is AttackSound:
                    object.play()


attack_normal_hit_sound = AttackSound(os.path.join(".", "assets", "sounds", "attack_normal_hit1.ogg"), 80)
attack_upper_hit_sound = AttackSound(os.path.join(".", "assets", "sounds", "attack_upper_hit.ogg"), 70)
demon_attack_hit_sound = AttackSound(os.path.join(".", "assets", "sounds", "demon_attack_hit.ogg"), 70)
imp_attack_hit_sound = AttackSound(os.path.join(".", "assets", "sounds", "imp_attack_hit.ogg"), 100)
