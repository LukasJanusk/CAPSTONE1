import pygame
from dataclasses import dataclass
from typing import List, Union
from . import animations
from . import enemies
from . import layer

class Sound_controller:
    @classmethod
    def play_sound(cls, layers: List[Union[animations.Animation, enemies.Enemy, layer.Layer]] = []):
        for sound in layers:



@dataclass
class Sound:
    sound_file: pygame.mixer.Sound
    start_frame: int
    end_frame: int = None
    