from dataclasses import dataclass
import pygame
import random
import math
import sys
import string
pygame.init()


blood_colours = [
    (204, 0, 0),
    (153, 0, 0),
    (128, 0, 0),
    (102, 0, 0),
    (77, 0, 0),
    (51, 0, 0),
]


@dataclass
class Particle:
    id: str
    position: tuple[int, int]
    colour: tuple
    last_update: int = pygame.time.get_ticks()
    speed: float = 0
    vertical_speed: float = 0
    gravity: float = 0
    facing_right = True


@dataclass
class Circle(Particle):
    radius: int = 10

    def get_vector_right(self) -> tuple[int, int]:
        angle = random.uniform(-math.pi / 2, math.pi / 2)
        vector_x = int(self.radius * math.cos(angle))
        vector_y = int(self.radius * math.sin(angle))
        return (vector_x, vector_y)

    def get_vector_left(self) -> tuple[int, int]:
        angle = random.uniform(math.pi / 2, 3 * math.pi / 2)
        vector_x = int(self.radius * math.cos(angle))
        vector_y = int(self.radius * math.sin(angle))
        return (vector_x, vector_y)

    def get_speed(self, vector_position: tuple):
        vector_x, vector_y = vector_position
        x, y = self.position
        speed = (vector_x - x) / 100
        vertical_speed = (vector_y - y) / 40
        return (speed, vertical_speed)

    @staticmethod
    def get_random_position_on_circle(radius: int) -> tuple[float, float]:
        angle = random.uniform(0, 2 * math.pi)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        return (x, y)

    @staticmethod
    def generate_cicles(
        n: int,
        colour: tuple[int, int, int],
        position: tuple[int, int],
        facing_right: bool = None,
        radius: int = 2,
        speed: float = 6,
        gravity: float = 0.1
                        ) -> list:
        circles = []
        for particle in range(n):
            name = f"{particle}" + str(random.choices(string.digits, k=5))
            circle = Circle(
                name,
                position,
                colour,
                radius=radius,
                speed=speed,
                gravity=gravity
                )
            if facing_right is not None:
                circle.vertical_speed = float(random.randint(-20, -10)/10)
                circle.facing_right = facing_right
                if not circle.facing_right:
                    circle.speed *= -1
            circles.append(circle)
        return circles

    def update_position(self):
        if self.facing_right:
            if self.speed <= 0:
                self.speed += self.gravity
        elif not self.facing_right:
            if self.speed >= 0:
                self.speed -= self.gravity
        x, y = self.position
        x += self.speed
        self.vertical_speed += self.gravity
        y += self.vertical_speed
        x += random.randint(-2, 2)
        self.position = (x, y)

    def decrease_size(self, decay: float = 0.1):
        self.radius -= decay

    def increase_size(self, expansion: float = 0.1):
        self.radius += expansion

    def update_existance(self):
        if self.radius <= 1:
            return False

    def render_circle(self, screen: pygame.surface.Surface):
        pygame.draw.circle(screen, self.colour, self.position, self.radius)


@dataclass
class Line(Particle):
    vector_x: int = None
    vector_y: int = None


def main():
    font = pygame.font.Font(size=25)
    screen = pygame.display.set_mode(
        (800, 640),
        pygame.HWSURFACE |
        pygame.RESIZABLE |
        pygame.DOUBLEBUF
        )
    clock = pygame.time.Clock()
    circles = []
    list = []
    colors = [
        (204, 0, 0),
        (153, 0, 0),
        (128, 0, 0),
        (102, 0, 0),
        (77, 0, 0),
        (51, 0, 0),
        (26, 0, 0),
        (13, 0, 0),
        (5, 0, 0)
    ]

    while True:
        random_red = random.choice(colors)
        mouse_pos = pygame.mouse.get_pos()
        x, y = mouse_pos
        pos1 = (x + 10, y + 80)
        pos2 = (x - 10, y + 70)
        pos3 = (x + 15, y + 45)
        pos4 = (x - 5, y + 60)
        pos5 = (x + 5, y + 100)
        pos6 = (x - 10, y + 100)
        pos7 = (x + 3, y + 90)
        positions = [pos1, pos2, pos3, pos4, pos5, pos6, pos7]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    list = Circle.generate_cicles(
                        random.randint(5, 30),
                        random_red,
                        random.choice(positions),
                        random.choice([True]),
                        6,
                        )
                    circles += list
        fps = int(clock.get_fps())
        font_surf = font.render(str(fps), True, (255, 255, 255))
        screen.fill((120, 120, 120))
        for circle in circles:
            circle.update_position()
            circle.decrease_size(0.2)
            x, y = circle.position
            if circle.update_existance() is False or y > 550:
                if len(circles) < 500:
                    maybe = random.choice([True, False])
                    if maybe:
                        list = Circle.generate_cicles(
                            1,
                            random_red,
                            circle.position,
                            random.choice([True, False]),
                            random.randint(2, 6),
                            speed=(random.randint(10, 100)/100)
                            )
                        circles += list
                circles.remove(circle)
        for circle in circles:
            circle.render_circle(screen)
            print(len(circles))
        screen.blit(font_surf, (10, 10))
        pygame.display.flip()

        clock.tick(90)


if __name__ == "__main__":
    main()
