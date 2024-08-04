import pygame
import os
import cProfile
from . import model
from .view import View
pygame.init()


def main():
    height = 640
    width = 800
    pygame.display.set_caption("game")
    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    font = pygame.font.Font(os.path.join(".", "assets", "fonts", "font.otf"), 18)
    clock = pygame.time.Clock()
    engine = model.Model()
    engine.load_user()
    profile = cProfile.Profile()
    profile.enable()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                profile.disable()
                profile.print_stats(sort="time")
                engine.save_and_quit()
            if engine.in_menu:
                engine.run_menus(event)
            if engine.in_game:
                engine.get_player_input(event)
        if engine.in_menu:
            View.draw_menus(screen, engine.menu_manager.current_menu)
        if engine.in_game:
            engine.controller.set_player_state()
            engine.get_current_level_wave()
            engine.update_enemies()
            engine.update_player()
            engine.update_scroll()
            engine.calculate_attacks()
            View.render(screen, engine.get_layers_for_blit())
            View.draw_player_hitbox(screen, engine.character)
            View.draw_player_attack_hitbox(screen, engine.character)
            View.draw_enemies_hitboxes(screen,
                                       engine.current_level.current_wave_enemies)
            View.draw_fps(screen, font, int(clock.get_fps()))
            View.draw_wave_number(screen,
                                  pygame.font.Font(os.path.join(".", "assets", "fonts", "font.otf"), 25),
                                  engine.current_level.waves,
                                  engine.current_level.current_wave
                                  )
        pygame.display.flip()
        clock.tick(120)


if __name__ == "__main__":
    main()
