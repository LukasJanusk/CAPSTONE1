import pygame
import os
from spritesheets import SpriteSheets
from dataclasses import dataclass

pygame.init()
width = 800
height = 640
screen = pygame.display.set_mode((width, height))


@dataclass
class Layer(SpriteSheets):
    _IMAGE: pygame.Surface
    scroll_multiplier: float = 1
    x: int = 0
    y: int = 0
    distance: float = 0
    scroll: float = 0
    frame: int = 0
    width: int = 0

    def __post_init__(self):
        self.width = self._IMAGE.get_width()
        self.sheet = self._IMAGE
        self._IMAGE = self.get_image(self.frame, self.width, height, 1, (150, 150, 150))
        # self._IMAGE.convert()
        # self._IMAGE.set_colorkey((150, 150, 150))
        # self._IMAGE.blit(screen, (0, 0))


# level0
level0_layer0 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "training_clouds_bg.png")),
                      scroll=-1)
level0_layer1 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "training_bg.png")))

# level1
level1_layer0 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level1_layer0.png")), scroll_multiplier=0.1)
level1_layer1 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level1_layer1.png")), scroll=-1, scroll_multiplier=0.2)
level1_layer2 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level1_layer2.png")), scroll_multiplier=0.4)
level1_layer3 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level1_layer3.png")), scroll=-1.5, scroll_multiplier=0.5)
level1_layer4 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level1_layer4.png")), scroll_multiplier=0.7)
level1_layer5 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level1_layer5.png")))
level1_layer6 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level1_layer6.png")))
level1_layer7 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level1_layer7.png")), scroll_multiplier=1.5)

# level3
level3_layer0 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level3_layer0.png")), scroll_multiplier=0.1)
level3_layer1 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level3_layer1.png")), scroll_multiplier=0.2)
level3_layer2 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level3_layer2.png")), scroll_multiplier=0.4)
level3_layer3 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level3_layer3.png")), scroll_multiplier=0.6)
level3_layer4 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level3_layer4.png")), scroll_multiplier=0.8)
level3_layer5 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level3_layer5.png")))
level3_layer6 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level3_layer6.png")), scroll_multiplier=1.2)
level3_layer7 = Layer(pygame.image.load(os.path.join("..", "assets", "graphics", "levels", "level3_layer7.png")), scroll_multiplier=1.5)
