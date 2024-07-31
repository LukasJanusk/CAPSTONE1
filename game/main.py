import pygame
import sys
import model
from view import View
from player import char


def main():
    pygame.init()
    height = 640
    width = 800
    pygame.display.set_caption("game")
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    engine = model.Model()
    char.idle = True
    char.current_animation = char.IDLE_ANIMATION
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            engine.get_player_input(event)
        screen.fill((110, 110, 110))
        engine.update_player()
        View.render(screen, [char])
        pygame.display.update()
        print(char.jumping)
        clock.tick(60)


if __name__ == "__main__":
    main()
