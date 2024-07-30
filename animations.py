import pygame
from dataclasses import dataclass
import spritesheets


@dataclass
class Animation:
    animation_list: list
    x: int
    y: int
    buffer_facing_left_x: int = 0
    buffer_facing_left_y: int = 0
    color_key: tuple

    def animate(self, game_screen, frame, facing_right):
        if frame > (len(self.animation_list) - 1): # to prevent out of bound errors
            frame = 0
        if facing_right:
            game_screen.blit(self.animation_list[frame], (self.x, self.y + self.buffer_facing_left_y))
        else:
            image = self.animation_list[frame]
            flipped_image = pygame.transform.flip(image, True, False)
            flipped_image.set_colorkey(self.color_key)
            game_screen.blit(flipped_image, (self.x + self.buffer_facing_left_x, self.y + self.buffer_facing_left_y))
        return True
