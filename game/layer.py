import pygame

pygame.init()


class Layer:
    def __init__(self, image, scroll_speed, x, y):
        self.x: int = x
        self.y: int = y
        self._IMAGE = pygame.image.load(f"graphics/levels/{image}").convert()
        self.distance: float = 0
        self.scroll_speed: float = scroll_speed
        self.frame: int = 0
        self.width: int = self._IMAGE.get_width()


# bamboo level layers
bamboo_0 = Layer()
bamboo_1 = None


# church level layers
