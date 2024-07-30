import pygame

class View:
    def __init__(self):
        self.player = Player: player
        self.layers: list = []
        self.level = Level: level


    def draw(self):
        for layer in self.layers:
            if layer != None:
                self.draw_layer()
    
    def draw_layer(self, screen):
        screen.blit()
        
    def print_layers(self, bg_images, game_screen, screen_width, bg_width):

        # scroll_for_layers = [{"layer": 0, "scroll": -2, "current_scroll": 0, "distance": 0},
        #                      {"layer": 1, "scroll": 0, "current_scroll": 0, "distance": 0}]


        tiles = math.ceil(screen_width / bg_width) + 1

        for image in bg_images:
            if bg_images.index(image) == 0:            
                tiles = math.ceil(screen_width/ bg_width) +1
                for i in range(tiles):
                    game_screen.blit(image, (i * bg_width + self.current_distance_layer0, 0))
                    game_screen.blit(image, (-i * bg_width + self.current_distance_layer0, 0)) 
                    #here print objects of level(enemies, player, objects, particles )
            else:
                tiles = math.ceil(screen_width/ bg_width) +1
                for i in range(tiles):
                    game_screen.blit(image, (i * bg_width + self.current_distance_layer1, 0))
                    game_screen.blit(image, (-i * bg_width + self.current_distance_layer1, 0)) 
        if abs(self.current_distance_layer0) > bg_width:
            self.current_distance_layer0 = 0
        if abs(self.current_distance_layer1) > bg_width:
            self.current_distance_layer1 = 0