import pygame
from dataclasses import dataclass
import os

height = 640
width = 800
screen = pygame.display.set_mode((width, height))


@dataclass
class SpriteSheets(pygame.sprite.Sprite):
    sheet: pygame.Surface

    def get_image(
            self,
            frame: int,
            width: int,
            height: int,
            scale:  int,
            colour: tuple
            ) -> pygame.surface.Surface:
        image = pygame.Surface((width, height)).convert()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image

    def get_animation_list(
            self, width: int, height: int, scale: float, colorkey: tuple, frames: int):
        temp_list = []
        for i in range(frames):
            temp_list.append(self.get_image(i, width, height, scale, colorkey))
        return temp_list


""" PLAYER ANIMATION EXTRACTION """
# Loading Spritesheet images
sprite_sheet_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "stick_idle.png"))
sprite_walk_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "stick_walk.png"))
sprite_guard_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "stick_guard.png"))
sprite_jump_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "stick_jump.png"))
sprite_jumping_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "stick_jumping.png"))
sprite_attack_upper_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "upper_attack.png"))
sprite_attack_normal_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "stick_attack_normal.png"))
sprite_attack_upper_phoenix_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "upper_attack_phoenix.png"))


# Creating Spritesheet object
sprite_attack_upper_phoenix_sheet = SpriteSheets(sprite_attack_upper_phoenix_image)
sprite_attack_normal_sheet = SpriteSheets(sprite_attack_normal_image)
sprite_attack_upper_sheet = SpriteSheets(sprite_attack_upper_image)
sprite_idle_sheet = SpriteSheets(sprite_sheet_image)
sprite_walk_sheet = SpriteSheets(sprite_walk_image)
sprite_guard_sheet = SpriteSheets(sprite_guard_image)
sprite_jump_sheet = SpriteSheets(sprite_jump_image)
sprite_jumping_sheet = SpriteSheets(sprite_jumping_image)

# sprite images as a list
idle_animation_list = sprite_idle_sheet.get_animation_list(
    50, 50, 2.5, (150, 150, 150), 9)
walking_animation_list = sprite_walk_sheet.get_animation_list(
    50, 60, 2.4, (150, 150, 150), 6)
guard_animation_list = sprite_guard_sheet.get_animation_list(
    50, 50, 2.5, (150, 150, 150), 4)
jump_animation_list = sprite_jump_sheet.get_animation_list(
    50, 50, 2.5, (150, 150, 150), 5)
jumping_animation_list = sprite_jumping_sheet.get_animation_list(
    50, 50, 2.5, (150, 150, 150), 5)
attack_upper_list = sprite_attack_upper_sheet.get_animation_list(
    111, 68, 2.5, (150, 150, 150), 14)
attack_normal_list = sprite_attack_normal_sheet.get_animation_list(
    70, 53, 2.5, (150, 150, 150), 7)
attack_upper_phoenix_list = []


"""ENEMIES SPRITESHEETS"""

# ===== demon =====

# idle
demon_idle_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "demon_idle.png"))
demon_idle_sheet = SpriteSheets(demon_idle_image)
demon_idle_animation_list = demon_idle_sheet.get_animation_list(500, 500, 1, (150, 150, 150), 4)
# running
demon_running_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "demon_running.png"))
demon_running_sheet = SpriteSheets(demon_running_image)
demon_running_animation_list = demon_running_sheet.get_animation_list(
    500, 500, 1, (150, 150, 150), 4)
# attack
demon_attack_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "demon_attack.png"))
demon_attack_sheet = SpriteSheets(demon_attack_image)
demon_attack_animation_list = demon_attack_sheet.get_animation_list(
    500, 500, 1, (150, 150, 150), 9)
# hit
demon_hit_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "demon_hit.png"))
demon_hit_sheet = SpriteSheets(demon_hit_image)
demon_hit_animation_list = demon_hit_sheet.get_animation_list(
    500, 500, 1, (150, 150, 150), 5)
# stunned
# death
demon_death_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "demon_death.png"))
demon_death_sheet = SpriteSheets(demon_death_image)
demon_death_animation_list = demon_death_sheet.get_animation_list(
    500, 500, 1, (150, 150, 150), 7)
# guarding

demon_animations = [
    demon_idle_animation_list,
    demon_hit_animation_list,
    demon_death_animation_list,
    demon_attack_animation_list,
    demon_running_animation_list
    ]

# ===== imp =====

# idle
imp_idle_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "imp_idle.png"))
imp_idle_sheet = SpriteSheets(imp_idle_image)
imp_idle_animation_list = imp_idle_sheet.get_animation_list(
    150, 150, 1, (150, 150, 150), 5)
# running
imp_running_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "imp_walking.png"))
imp_running_sheet = SpriteSheets(imp_running_image)
imp_running_animation_list = imp_running_sheet.get_animation_list(
    150, 150, 1, (150, 150, 150), 5)
# attack
imp_attack_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "imp_attack.png"))
imp_attack_sheet = SpriteSheets(imp_attack_image)
imp_attack_animation_list = imp_attack_sheet.get_animation_list(
    150, 150, 1, (150, 150, 150), 5)
# hit
imp_hit_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "imp_hit.png"))
imp_hit_sheet = SpriteSheets(imp_hit_image)
imp_hit_animation_list = imp_hit_sheet.get_animation_list(
    150, 150, 1, (150, 150, 150), 7)
# stunned
# death
imp_death_image = pygame.image.load(
    os.path.join(".", "assets", "graphics", "sprites", "imp_death.png"))
imp_death_sheet = SpriteSheets(imp_death_image)
imp_death_animation_list = imp_death_sheet = imp_death_sheet.get_animation_list(
    150, 150, 1, (150, 150, 150), 7)
# guarding

imp_animations = [
    imp_idle_animation_list,
    imp_hit_animation_list,
    imp_death_animation_list,
    imp_attack_animation_list,
    imp_running_animation_list
    ]

# ===== shade =====

# idle
# running
# attack
# hit
# stunned
# death
# guarding

# ===== charger =====

# idle
# running
# attack
# hit
# stunned
# death
# guarding
