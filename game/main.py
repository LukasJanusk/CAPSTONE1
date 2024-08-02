import pygame
import sys
import model
from view import View
import cProfile

pygame.init()


def main():
    height = 640
    width = 800
    pygame.display.set_caption("game")
    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    clock = pygame.time.Clock()
    engine = model.Model()
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
        engine.update_player()
        engine.calculate_attacks()
        View.render(screen, engine.get_layers_for_blit())
        # if engine.character.current_attack is not None:
        #     engine.character.current_attack.draw_hitbox(screen, engine.character.frame)
        View.draw_player_hitbox(screen, engine.character)
        View.draw_player_attack_hitbox(screen, engine.character)
        View.draw_enemies_hitboxes(screen, engine.current_level.current_wave_enemies)
        pygame.display.flip()
        clock.tick(120)


if __name__ == "__main__":
    main()
