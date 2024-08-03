from dataclasses import dataclass
import pygame
import os
pygame.init()


@dataclass
class Button:
    NAME: str
    x: int = 0
    y: int = 0
    text_colour: tuple = (0, 0, 0)
    hover_colour: tuple = (20, 145, 100)
    clicked_colour: tuple = (50, 225, 100)
    font: pygame.font.Font = None
    font_size: int = 40
    hover: bool = False
    clicked: bool = False
    surface: pygame.Surface = None
    rect: pygame.Rect = None

    def __post_init__(self):
        self.font = pygame.font.Font(os.path.join(".", "assets", "fonts", "font.otf"), self.font_size)
        self.surface = self.font.render(self.NAME, True, (0, 0, 0))
        self.rect = self.surface.get_rect()

    def center_button(self, screen: pygame.Surface):
        screen_rect = screen.get_rect()
        self.x = (screen_rect.width - self.rect.width) // 2

    def update_colour(self):
        if self.hover:
            self.surface = self.font.render(self.NAME, True, self.hover_colour)
        else:
            self.surface = self.font.render(self.NAME, True, self.text_colour)


quit_button = Button("QUIT")
back_button = Button("BACK", y=510)
new_game_button = Button("NEW GAME")
high_scores_button = Button("HIGHSCORES")
settings_button = Button("SETTINGS")
level0_button = Button("TESTING")
level1_button = Button("LEVEL 1")
level2_button = Button("LEVEL 2")
level3_button = Button("LEVEL 3")
level4_button = Button("LEVEL 4")
level5_button = Button("Level 5")
continue_button = Button("CONTINUE")


@dataclass
class Menu:
    NAME: str
    active: bool = False
    x: int = 0
    y: int = 0
    text_x: int = 0
    text_y: int = 20
    colour: tuple = (27, 82, 108)
    text_colour: tuple = (0, 0, 0)
    font: pygame.font.Font = None
    font_size: int = 80
    buttons: list = None
    selected_button: Button = None
    text_surface: pygame.Surface = None
    text_rect: pygame.rect.Rect = None

    def __post_init__(self):
        self.font = pygame.font.Font(os.path.join(".", "assets", "fonts", "font.otf"), self.font_size)
        self.text_surface = self.font.render(self.NAME, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.selected_button = self.buttons[0]

    def center_text(self, screen: pygame.Surface):
        screen_rect = screen.get_rect()
        self.text_x = (screen_rect.width - self.text_rect.width) // 2


user_select_menu = Menu("SELECT USER", buttons=[quit_button])
main_menu = Menu("MAIN MENU", buttons=[new_game_button, high_scores_button, settings_button, quit_button])
settings_menu = Menu("SETTINGS", buttons=[back_button])
high_scores_menu = Menu("HIGHSCORES", buttons=[back_button])
new_game_menu = Menu("NEW GAME", buttons=[level0_button, level1_button, level2_button, level3_button, level4_button, level5_button, back_button])
pause_menu = Menu("PAUSE", buttons=[continue_button, main_menu, quit_button])


@dataclass
class Menu_Controller:
    user = None
    active: bool = True
    menus = []
    current_menu: Menu = None

    def __post_init__(self):
        self.current_menu = main_menu
        self.current_menu.active = True

    def get_active_button(self, event: pygame.event.Event):
        first = 0
        last = len(self.current_menu.buttons) - 1
        index = self.current_menu.buttons.index(self.current_menu.selected_button)
        index = self.get_index(index, event)
        if index > last:
            index = first
        if index < first:
            index = last
        for index_of_button, button in enumerate(self.current_menu.buttons):
            if index_of_button == index:
                button.hover = True
                self.current_menu.selected_button = button
            else:
                button.hover = False
            button.update_colour()

    def get_index(self, index,  event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                index -= 1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                index += 1
        return index

    def set_active_menu(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.current_menu == main_menu:
                    if self.current_menu.selected_button == new_game_button:
                        self.current_menu.active = False
                        self.current_menu = new_game_menu
                        self.current_menu.active = True
                    elif self.current_menu.selected_button == settings_button:
                        self.current_menu.active = False
                        self.current_menu = settings_menu
                        self.current_menu.active = True
                    elif self.current_menu.selected_button == high_scores_button:
                        self.current_menu.active = False
                        self.current_menu = high_scores_menu
                        self.current_menu.active = True
                    elif self.current_menu.selected_button == quit_button:
                        return "quit"
                elif self.current_menu == new_game_menu:
                    if self.current_menu.selected_button == back_button:
                        self.current_menu.active = False
                        self.current_menu = main_menu
                        self.current_menu.active = True
                    elif self.current_menu.selected_button == level3_button:
                        self.current_menu.active = False
                        return "level3"


menu_controller = Menu_Controller([user_select_menu, main_menu, settings_menu, high_scores_menu, new_game_menu, pause_menu])

