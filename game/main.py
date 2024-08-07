import pygame
import cProfile
from . import model
from .view import View
pygame.init()


def main():
    height = 640
    width = 800
    pygame.display.set_caption("game")
    screen = pygame.display.set_mode(
        (width, height),
        pygame.HWSURFACE |
        pygame.DOUBLEBUF |
        pygame.RESIZABLE
        )
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
                engine.pause_game(event)
                engine.get_player_input(event)
        if engine.in_menu:
            View.draw_menus(
                screen,
                engine.menu_manager.current_menu,
                engine.user
                )
        if engine.in_game:
            engine.controller.set_player_state()
            engine.run_enemies_ai()
            engine.get_current_level_wave()
            engine.update_enemies()
            engine.update_particles()
            engine.check_for_level_end()
            engine.update_player()
            engine.update_scroll()
            engine.calculate_attacks()
            View.render(
                screen,
                str(engine.current_level.score),
                engine.get_layers_for_blit(),
                draw_hitboxes=engine.settings.draw_hitboxes,
                draw_health_bars=engine.settings.draw_health_bar,
                draw_particles=engine.settings.draw_particles)
            # engine.print_particles_n()
            if engine.settings.draw_fps:
                View.draw_fps(screen, int(clock.get_fps()))
            View.draw_wave_number(
                screen,
                engine.current_level.total_waves,
                engine.current_level.current_wave
                )
        pygame.display.flip()
        clock.tick(90)


if __name__ == "__main__":
    main()
