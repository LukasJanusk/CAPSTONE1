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
class Ember(Circle):
    colours = fire_colours = [
        (255, 69, 0),
        (255, 140, 0),
        (255, 165, 0),
        (255, 215, 0),
        (255, 255, 102),
        (255, 255, 224),
        (255, 255, 240)
        ]
    colour = random.choice(blood_colours)
    vertical_speed = 3
    speed: float = 2
    gravity: float = 0
    atmosphere = 0

    @classmethod
    def generate_embers(
        cls,
        n: int,
        position: tuple[int, int],
        radius: int,
        discrepency: int,
        facing_right: bool
            ) -> list:
        """Generates ember particles"""
        embers = []
        for i in range(n):
            ember = Ember(
                id=i,
                position=position,
                colour=random.choice(cls.colours),
                speed=cls.speed,
                vertical_speed=cls.speed,
                gravity=cls.gravity,
                atmosphere=cls.atmosphere,
                facing_right=facing_right,
                radius=radius + random.choice((-discrepency, discrepency)),
            )
            embers.append(ember)
        return embers


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
    length: int = 2
    width: int = 4
    vector: tuple = None
    angle: float = None
    colours = [
        (173, 216, 230),  # Light Blue
        (192, 226, 238),  # Slightly lighter blue
        (211, 237, 245),  # Very light blue
        (230, 247, 252),  # Almost white with a hint of blue
        (240, 252, 255),  # Very faint blue, close to white
        (255, 255, 255)   # White
    ]

    def __post_init__(self):
        # Determine the angle based on the direction
        if self.facing_right:
            self.angle = random.uniform(0, 90) if random.choice([True, False]) else random.uniform(270, 360)
        else:
            self.angle = random.uniform(90, 270)

        x, y = self.position
        self.vector = (x + self.length, y + self.length)

    def calculate_random_vector(self, range: int) -> None:
        self.position = self.vector
        random_angle = self.angle + random.uniform(-range, range)
        random_angle_rad = math.radians(random_angle)
        x_component = self.length * math.cos(random_angle_rad)
        y_component = self.length * math.sin(random_angle_rad)

        x, y = self.position
        new_x = x + x_component
        new_y = y + y_component

        self.vector = (int(new_x), int(new_y))

    def render_line(self, screen: pygame.surface.Surface) -> None:
        pygame.draw.line(
            screen,
            random.choice(self.colours),
            self.position,
            self.vector,
            self.width
        )

    @classmethod
    def generate_lines(cls, n: int, position: tuple[int, int], facing_right: bool):
        """Generates line particles"""
        lines = []
        for i in range(n):
            line = Line(
                id=i,
                position=position,
                colour=random.choice(cls.colours),
                speed=1,
                vertical_speed=0,
                facing_right=facing_right,
                length=2,
                atmosphere=0.2,
                gravity=random.randint(-10, 10) / 10,
            )
            lines.append(line)
        return lines


def main():
    font = pygame.font.Font(size=25)
    screen = pygame.display.set_mode(
        (800, 640),
        pygame.HWSURFACE |
        pygame.RESIZABLE |
        pygame.DOUBLEBUF
        )
    clock = pygame.time.Clock()
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
                    list = Blood.generate_blood(15, mouse_pos, 6, 2, False)
                    list_square = BlockSquare.generate_block_squares(15, mouse_pos, 15)
                    line_list = Line.generate_lines(15, mouse_pos, True)
                    embers_list = Ember.generate_embers(15, mouse_pos, 4, 1, True)
                    particles += line_list
                    particles += list
                    particles += list_square
                    particles += embers_list
        fps = int(clock.get_fps())
        font_surf = font.render(str(fps), True, (255, 255, 255))
        screen.fill((120, 120, 120))
        for particle in particles:
            if type(particle) is Circle or type(particle) is Blood or type(particle) is Ember:
                particle.decrease_size(0.05)
                particle.update_position()
                if particle.update_existance() is False:
                    particles.remove(particle)
                else:
                    x, y = particle.position
                    if y > 560 and type(particle) is not BlockSquare:
                        splash_list = Blood.generate_blood_splash(particle.position, float(particle.radius))
                        particles += splash_list
                        particles.remove(particle)
            if type(particle) is BlockSquare:
                particle.decrease_size(0.5)
                particle.update_position()
                if particle.width < 1:
                    particles.remove(particle)
            if type(particle) is Line:
                particle.calculate_random_vector(10)
                particle.update_position()
                particle.length += 0.5
                if particle.length > 30 or particle. width < 1:
                    particles.remove(particle)
        for particle in particles:
            if type(particle) is Circle or type(particle) is Blood or type(particle) is Ember:
                particle.render_circle(screen)
            elif type(particle) is Square or type(particle) is BlockSquare:
                x, y = particle.position
                rect = pygame.rect.Rect(x, y, particle.width, particle.height)
                pygame.draw.rect(screen, particle.colour, rect)
            elif type(particle) is Line:
                particle.render_line(screen)
        screen.blit(font_surf, (10, 10))
        pygame.display.flip()
        print(len(particles))

        clock.tick(90)


if __name__ == "__main__":
    main()
