import pygame
from dataclasses import dataclass



@dataclass
class Input_controller():
    user_text = ""

    def get_user_input(self, event:pygame.event.Event):
        