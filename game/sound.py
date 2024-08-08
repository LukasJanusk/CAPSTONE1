import pygame
import os
from typing import List, Union
pygame.mixer.init()


class HitSound(pygame.mixer.Sound):
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


class AnimationSound(HitSound):
    def __init__(self, file, downtime: int, start_frame: int, maximum_duration: int = 2000):
        super().__init__(file, downtime)
        self.frame = start_frame
        self.maximum_duration = maximum_duration


class Sound_Controller:
    @staticmethod
    def play_sounds(
        objects: List[Union[
            HitSound,
            AnimationSound,
           ]]):
        if objects is not None or objects != []:
            for object in objects:
                if type(object) is AnimationSound:
                    object.play(maxtime=object.maximum_duration)
                elif type(object) is HitSound:
                    object.play()


# attack hit sounds
attack_normal_hit_sound = HitSound(os.path.join(".", "assets", "sounds", "attack_normal_hit1.ogg"), 80)
attack_upper_hit_sound = HitSound(os.path.join(".", "assets", "sounds", "attack_upper_hit.ogg"), 70)
demon_attack_hit_sound = HitSound(os.path.join(".", "assets", "sounds", "demon_attack_hit.ogg"), 70)
imp_attack_hit_sound = HitSound(os.path.join(".", "assets", "sounds", "imp_attack_hit.ogg"), 100)

# hit sounds
player_hit_sound = HitSound(os.path.join(".", "assets", "sounds", "player_hit_sound.ogg"), 500)
demon_hit_sound = HitSound(os.path.join(".", "assets", "sounds", "demon_hit_sound.ogg"), 2500)
imp_hit_sound = HitSound(os.path.join(".", "assets", "sounds", "imp_hit_sound.ogg"), 1000)
# death sounds

# Animation sounds
attack_upper_sound1 = AnimationSound(
    os.path.join(
        ".", "assets", "sounds", "attack_upper_sound1.ogg"),
    300,
    7
    )
attack_upper_sound2 = AnimationSound(
    os.path.join(
        ".", "assets", "sounds", "attack_upper_sound1.ogg"),
    300,
    8,
    )
attack_normal_sound1 = AnimationSound(
    os.path.join(
        ".", "assets", "sounds", "attack_normal_sound1.ogg"),
    150,
    1,
    maximum_duration=160
    )
attack_normal_sound2 = AnimationSound(
    os.path.join(
        ".", "assets", "sounds", "attack_normal_sound1.ogg"),
    150,
    3,
    maximum_duration=160
    )
