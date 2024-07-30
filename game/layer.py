import pygame


class Layer:
    def __init__(self, image, scroll, x, y):
        self.x: int = x
        self.y: int = y
        self._IMAGE = pygame.image.load(f"graphics/levels/{image}").convert()
        self._SCROLL: float = scroll
        self.frame: int = 0


# bamboo level layers
bamboo_0 = Layer()
bamboo_1 = None


# church level layers
