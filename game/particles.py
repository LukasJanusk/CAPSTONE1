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

blue_colours = [
    (0, 0, 255),
    (0, 51, 204),
    (0, 77, 153),
    (0, 102, 204),
    (0, 128, 255),
]


@dataclass
class Particle:
    id: str
    position: tuple[int, int]
    colour: tuple
    speed: float = 0
    vertical_speed: float = 0
    gravity: float = 0
    atmosphere: float = 0
    facing_right: bool = None

    @staticmethod
    def get_random_position_in_rect(rect: pygame.rect.Rect) -> tuple:
        x = random.randint(rect.x, rect.x + rect.width)
        y = random.randint(rect.y, rect.y + rect.height)
        return (x, y)

    @staticmethod
    def get_collision_rect(
        rect1: pygame.rect.Rect,
        rect2: pygame.rect.Rect
            ) -> pygame.rect.Rect:
        if rect1.colliderect(rect2):
            return rect1.clip(rect2)
        return None

    def update_position(self):
        if not self.speed <= 0:
            if self.facing_right:
                self.speed -= self.atmosphere
        self.vertical_speed -= self.gravity
        x, y = self.position
        y -= self.vertical_speed
        x += self.speed
        self.position = (x, y)


@dataclass
class Circle(Particle):
    radius: float = 10

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
                circle.vertical_speed = float(random.randint(-20, 10)/10)
                circle.facing_right = facing_right
                if not circle.facing_right:
                    circle.speed *= -1
            circles.append(circle)
        return circles

    def decrease_size(self, decay: float = 0.1):
        self.radius -= decay

    def increase_size(self, expansion: float = 0.1):
        self.radius += expansion

    def update_existance(self) -> bool | None:
        x, y = self.position
        if y < 0 or y > 640:
            return False
        if x < - 800 or x > 2000:
            return False
        if self.radius <= 1:
            return False

    def render_circle(self, screen: pygame.surface.Surface):
        pygame.draw.circle(screen, self.colour, self.position, self.radius)


@dataclass
class Blood(Circle):
    colour = random.choice(blood_colours)
    vertical_speed = 3
    speed: float = 6
    gravity: float = 0.2
    atmosphere = 0.1
    blood_colours = [
        (204, 0, 0),
        (153, 0, 0),
        (128, 0, 0),
        (102, 0, 0),
        (77, 0, 0),
        (51, 0, 0),
    ]

    @classmethod
    def generate_blood(
        cls, n: int,
        position: tuple[int, int],
        radius: int,
        discrepency: int,
        facing_right: bool
            ) -> list:
        """Generates blood particles"""
        blood_particles = []
        blood_colour = random.choice(cls.blood_colours)
        for i in range(n):
            x, y = position
            # new_x = x + random.randint(-10, 10)
            # new_y = y + random.randint(-3, 3)
            new_x = x + i * 3
            new_y = y
            blood = Blood(
                i,
                (new_x, new_y),
                blood_colour,
                speed=random.randint(4, 6),
                vertical_speed=random.randint(-1, 3),
                facing_right=facing_right,
                radius=random.randint(radius - discrepency, radius + discrepency)
            )
            blood.facing_right = facing_right
            if not facing_right:
                blood.speed *= -1
            blood_particles.append(blood)
        return blood_particles

    @classmethod
    def generate_blood_splash(cls, position: tuple[int, int], radius: float) -> list:
        """Generates blood particles to simulate splash hitting the floor"""
        maybe = random.choice([True, False])
        if maybe:
            characters = string.digits + string.ascii_letters + string.punctuation
            id = ''.join(random.choices(characters, k=5))
            i_x, i_y = position
            new_position = (int(i_x + random.randint(-2, 2)), int(i_y + random.randint(-2, 0)))
            if radius > 0.5:
                radius = radius - 0.5
            blood = Blood(
                id,
                new_position,
                random.choice(cls.blood_colours),
                speed=random.randint(-3, 3),
                vertical_speed=float(random.randint(1, 3)),
                gravity=0.2,
                facing_right=random.choice([True, False]),
                radius=radius)
            return [blood]
        return []


@dataclass
class Square(Particle):
    width: float = 1
    height: float = 1

    def increase_size(self, growth: float = 0.1):
        self.width += growth
        self.height += growth

    def decrease_size(self, decay: float = 0.1):
        self.width -= decay
        self.height -= decay

    def update_square_existance(self):
        if self.width <= 1 or self.height <= 1:
            return False


@dataclass
class BlockSquare(Square):
    colours = [
        (0, 0, 255),
        (0, 51, 204),
        (0, 77, 153),
        (0, 102, 204),
        (0, 128, 255),
    ]

    @classmethod
    def generate_block_squares(cls, n: int, position: tuple[int, int], size: int) -> list:
        """Genereats blue squares"""
        squares = []
        for i in range(n):
            x, y = position
            new_x = x + random.randint(-10, 10)
            new_y = y + random.randint(-10, 10)
            new_position = (new_x, new_y)
            if size > 4:
                size += random.randint(-3, 3)
            square = BlockSquare(
                id=i,
                position=new_position,
                width=size,
                height=size,
                colour=random.choice(cls.colours),
                speed=0,
                vertical_speed=0.1,
                gravity=0,
                atmosphere=0
            )
            squares.append(square)
        return squares


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
    particles = []
    list = []

    while True:
        mouse_pos = pygame.mouse.get_pos()
        x, y = mouse_pos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    list = Blood.generate_blood(10, mouse_pos, 10, 2, False)
                    particles += list
        fps = int(clock.get_fps())
        font_surf = font.render(str(fps), True, (255, 255, 255))
        screen.fill((120, 120, 120))
        for particle in particles:
            particle.update_position()
            particle.decrease_size(0.15)
            x, y = particle.position
            if particle.update_existance() is False:
                particles.remove(particle)
            elif y > 560:
                splash_list = Blood.generate_blood_splash(particle.position, float(particle.radius))
                particles += splash_list
                particles.remove(particle)
        for particle in particles:
            particle.render_circle(screen)
            print(len(circles))
        screen.blit(font_surf, (10, 10))
        pygame.display.flip()

        clock.tick(90)


if __name__ == "__main__":
    main()
