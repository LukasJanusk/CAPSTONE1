import pygame
import sys


def main():
    pygame.init()
    height = 640
    width = 800
    pygame.display.set_caption("Game")
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((110, 110, 110))
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
