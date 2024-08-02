import pygame
import sys
import model
from view import View
from player import char
import cProfile

pygame.init()


def main():
    height = 640
    width = 800
    pygame.display.set_caption("game")
    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    clock = pygame.time.Clock()
    engine = model.Model()
    char.idle = True
    char.current_animation = char.IDLE_ANIMATION
    profile = cProfile.Profile()
    profile.enable()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                profile.disable()
                profile.print_stats(sort="time")
                pygame.quit()
                sys.exit()
            engine.get_player_input(event)
        engine.controller.set_player_state()
        engine.update_scroll()
        # screen.fill((110, 110, 110))
        if char.frame == 3:
            char.health -= 1
        engine.update_player()
        View.render(screen, engine.get_layers_for_blit())
        pygame.display.flip()
        if char.frame == 0:
            print(char.health)
        clock.tick(120)
        # if char.frame == 0:
        #     print(f"FPS: {int(clock.get_fps())}")


if __name__ == "__main__":
    main()
