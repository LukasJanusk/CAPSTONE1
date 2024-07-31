import pygame
from player import Player, char


class Controller:
    def __init__(self):
        self.player: Player = char

    def set_player_states(self, event: pygame.event.Event):
        self.set_key_up_events(event)
        self.set_keydown_events(event)
        self.set_player_state()

    def set_key_up_events(self, event: pygame.event.Event):
        frame_reset_list = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_w, pygame.K_y, pygame.K_u, pygame.K_h]
        if event.type == pygame.KEYUP:
            if event.key in frame_reset_list:
                self.player.frame = 0
            if event.key == pygame.K_SPACE:
                self.player.guarding = False
                self.player.frame = 0
            if event.key == pygame.K_a:
                if not self.player.facing_right:
                    self.player.attack_moving = False
                    self.player.walking = False
                    self.player.running = False
            if event.key == pygame.K_d:
                if self.player.facing_right:
                    self.player.attack_moving = False
                    self.player.walking = False
                    self.player.running = False
            if event.key == pygame.K_y:
                self.player.attacking_upper = False
            if event.key == pygame.K_u:
                self.player.attacking_normal = False
            if event.key == pygame.K_LSHIFT:
                self.player.running = False

    def set_keydown_events(self, event):
        if not self.player.attacking_upper:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self.player.frame = 0

    def set_player_state(self):
        key = pygame.key.get_pressed()
        # jumping state actions and inputs
        if self.player.jumping is True:
            self.player.walking = False
            self.player.running = False
            self.player.guarding = False
            self.player. ducking = False
            if key[pygame.K_y] is True:
                self.player.attacking_upper = True
                self.player.aerial_movement = False
            elif key[pygame.K_u] is True:
                self.player.attacking_normal = True
            if key[pygame.K_d] is True:
                self.player.facing_right = True
                self.player.aerial_movement = True
            if key[pygame.K_a] is True:
                self.player.facing_right = False
                self.player.aerial_movement = True
        # walking state inputs
        elif self.player.walking is True:
            self.player.guarding = False
            self.player.attacking_normal = False
            self.player.attacking_upper = False
            self.player.jumping = False
            self.player.ducking = False
            self.player.running = False
            self.player.idle = False
        # trigger other states by inputs:
            if key[pygame.K_w] is True:
                self.player.jumping = True
                self.player.walking = False
            elif key[pygame.K_s] is True:
                self.player.ducking = True
                self.player.walking = False
            elif key[pygame.K_SPACE] is True:
                self.player.guarding = True
                self.player.walking = False
            elif key[pygame.K_y] is True:
                self.player.attacking_upper = True
                self.player.walking = False
            elif key[pygame.K_u] is True:
                self.player.attacking_normal = True
                self.player.walking = False
                if key[pygame.K_d] is True:
                    self.player.facing_right = True
                    self.player.attack_moving = True
                elif key[pygame.K_a] is True:
                    self.player.facing_right = False
                    self.player.attack_moving = True
            elif key[pygame.K_LSHIFT] is True:
                self.player.running = True
                self.player.walking = False
            if key[pygame.K_d] is True:
                self.player.facing_right = True
                if self.player.attacking_normal is True:
                    self.player.attack_moving = True
            if key[pygame.K_a] is True:
                self.player.facing_right = False
                if self.player.attacking_normal is True:
                    self.player.attack_moving = True
        # running state inputs
        elif self.player.running is True:
            # trigger other states by inputs:
            if key[pygame.K_w] is True:
                self.player.jumping = True
                self.player.running = False
            elif key[pygame.K_s] is True:
                self.player.ducking = True
                self.player.running = False
            elif key[pygame.K_SPACE] is True:
                self.player.guarding = True
                self.player.running = False
            elif key[pygame.K_y] is True:
                self.player.attacking_upper = True
                self.player.running = False
            elif key[pygame.K_u] is True:
                self.player.attacking_normal = True
                self.player.running = False
            elif key[pygame.K_LSHIFT] is True:
                self.player.running = True
            if key[pygame.K_d] is True:
                self.player.facing_right = True
            if key[pygame.K_a] is True:
                self.player.facing_right = False

        # guarding state inputs
        elif self.player.guarding is True:
            self.player.jumping is False
            self.player.walking = False
            self.player.running = False
            self.player. ducking = False
            self.player.attacking_normal = False
            self.player.attacking_upper = False
            if key[pygame.K_SPACE] is True:
                self.player.guarding = True
            if key[pygame.K_d] is True:
                self.player.facing_right = True
            if key[pygame.K_a] is True:
                self.player.facing_right = False
            if key[pygame.K_w] is True:
                self.player.jumping = True
                self.player.guarding = False
                # elif key[pygame.K_s] is True:
                #     self.player.ducking = True
                #     self.player.guarding = False
                # elif key[pygame.K_y] is True:
                #     self.player.attacking_upper = True
                #     self.player.guarding = False
                # elif key[pygame.K_u] is True:
                #     self.player.attacking_normal = True
                #     self.player.guarding = False
            # #elif dashing = True:
            #     pass
        elif self.player.attacking_normal is True:
            self.player.idle = False
            self.player.walking = False
            self.player.running = False
            self.player.attacking_upper = False
            self.player.ducking = False
            self.player.guarding = False
            if key[pygame.K_d] is True:
                self.player.facing_right = True
                self.player.attack_moving = True
            if key[pygame.K_a] is True:
                self.player.facing_right = False
                self.player.attack_moving = True
            if not self.player.jumping:
                if key[pygame.K_w] is True:
                    self.player.jumping = True
                if key[pygame.K_SPACE] is True:
                    self.player.guarding = True
                    self.player.attacking_normal = False
                if key[pygame.K_s] is True:
                    self.player.ducking = True
                if key[pygame.K_y] is True:
                    self.player.attacking_upper = True
                    self.player.attacking_normal = False

        elif self.player.attacking_upper is True:
            self.player.attacking_normal = False
            self.player.idle = False
            self.player.aerial_movement = False
            self.player.attack_moving = False
        elif self.player.ducking is True:
            pass

        # idle state inputs
        elif self.player.idle is True:
            self.player.guarding = False
            self.player.jumping = False
            self.player.aerial_movement = False
            self.player.attacking_normal = False
            self.player.attacking_upper = False
            self.player.walking = False
            self.player.running = False
            if key[pygame.K_w] is True:
                self.player.jumping = True
                self.player.idle = False
            elif key[pygame.K_s] is True:
                self.player.ducking = True
                self.player.idle = False
            elif key[pygame.K_SPACE] is True:
                self.player.guarding = True
                self.player.idle = False
            elif key[pygame.K_y] is True:
                self.player.attacking_upper = True
                self.player.idle = False
            elif key[pygame.K_u] is True:
                self.player.attacking_normal = True
                self.player.idle = False
                if key[pygame.K_d] is True:
                    self.player.facing_right = True
                    self.player.attack_moving = True
                elif key[pygame.K_a] is True:
                    self.player.facing_right = False
                    self.player.attack_moving = True
            elif key[pygame.K_d] is True:
                self.player.facing_right = True
                self.player.walking = True
                self.player.idle = False
            elif key[pygame.K_a] is True:
                self.player.facing_right = False
                self.player.walking = True
                self.player.idle = False
        else:
            self.player.idle = True

    # def update_speed(self):
    #     if not self.player.jumping:
    #         self.player.aerial_movement = False
    #     self.player.speed = 0
    #     if self.player.running is True:
    #         self.player.speed += 2.5
    #     if self.player.walking is True:
    #         self.player.speed += 1.5
    #     if self.player.dashing:
    #         self.player.speed += 4
    #     if self.player.attack_moving is True:
    #         self.player.speed += 0.4
    #     if self.player.aerial_movement is True:
    #         self.player.speed += 2
    #     if self.player.ducking is True:
    #         self.player.speed = 0
    #     if self.player.guarding is True:
    #         self.player.speed = 0
    #     if self.player.idle is True:
    #         self.player.speed = 0
    #     if self.player.facing_right:
    #         self.player.speed = self.player.speed * -1


player_input_manager = Controller()
