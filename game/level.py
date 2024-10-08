import pygame
from dataclasses import dataclass, field
import os
from typing import List, Union
from .enemies import Enemy, Demon, Imp
from . import layer
from .layer import Layer
from .objects import Health_Potion, Elemental_Orb
import random
available_enemies = ["demon", "imp"]
available_enemies_weights = [50, 100]
pygame.mixer.init()


@dataclass
class Level:
    name: str
    x: int = 0
    y: int = 0
    layer0: Layer = None
    layer1: Layer = None
    layer2: Layer = None
    layer3: Layer = None
    layer4: Layer = None
    layer5: Layer = None
    layer6: Layer = None
    layer7: Layer = None
    total_waves: int = 15
    current_wave: int = 0
    current_wave_enemies: List[
        Union[
            Enemy,
            Demon,
            Imp]
            ] = field(default_factory=list)
    objects: List[
        Union[
            Health_Potion,
            Elemental_Orb]
            ] = field(default_factory=list)
    _score: int = 0
    ambient_sound: pygame.mixer.Sound = None

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value):
        if type(value) is not int:
            raise TypeError("Score must be and Integer")
        if value < 0:
            raise ValueError("Score cannot be negative")
        else:
            self._score = value

    def is_colliding(self, new_enemy, wave: list) -> bool:
        return any(
            new_enemy.hitbox.colliderect(enemy_obj.hitbox) for enemy_obj in wave)

    def generate_dropable_items(self, chance: int, enemy: Enemy) -> None:
        """
        Generates pickable items based on the given drop chance.
        Args:
            chance (int): The drop rate, defined as a 1 in `chance` probability for an item to drop. Minimum `chance` should be 5
            enemy (enemies.Enemy): The enemy instance from which items may drop.
        """
        number = random.randint(1, chance)
        if number == 1:
            potion = Health_Potion(enemy.x + enemy.hitbox.width, 500)
            self.objects.append(potion)
        if number == 2:
            elemental_Orb = Elemental_Orb(enemy.x + enemy.hitbox.width, 500)
            self.objects.append(elemental_Orb)

    def generate_wave(self, player_x: int) -> bool | List[Union[
        Enemy,
        Demon,
        Imp,
        ]
            ]:
        """Return enemies wave"""
        wave = []
        for i in range(
            random.randint(
                (1 * self.current_wave + 1),
                2 * (self.current_wave + 1))
                ):

            choice = random.choices(
                available_enemies,
                weights=available_enemies_weights,
                k=1)[0]
            x = random.randint(int(player_x - 150), int(player_x + 1000))
            if choice == "demon":
                enemy = Demon(x, 50, name=str(i))
                while self.is_colliding(enemy, wave):
                    enemy.x += 50
                    enemy.update_hitbox()
                wave.append(enemy)
            elif choice == "imp":
                enemy = Imp(x, random.randint(320, 360), name=str(i))
                while self.is_colliding(enemy, wave):
                    enemy.x += 30
                    enemy.update_hitbox()
                wave.append(enemy)
            else:
                print("Failed to create enemy")
        self.current_wave += 1
        return wave

    def get_layers_list(self) -> List[Union[Layer]]:
        """Returns all ordered layers list for current level"""
        return [self.layer0,
                self.layer1,
                self.layer2,
                self.layer3,
                self.layer4,
                self.layer5,
                self.layer6,
                self.layer7]


level1 = Level("Museum",
               layer0=layer.level0_layer0,
               layer1=layer.level0_layer1)
level2 = Level("Hills",
               layer0=layer.level1_layer0,
               layer1=layer.level1_layer1,
               layer2=layer.level1_layer2,
               layer3=layer.level1_layer3,
               layer4=layer.level1_layer4,
               layer5=layer.level1_layer5,
               layer6=layer.level1_layer6,
               layer7=layer.level1_layer7)
level3 = Level("Bamboo forest",
               layer0=layer.level3_layer0,
               layer1=layer.level3_layer1,
               layer2=layer.level3_layer2,
               layer3=layer.level3_layer3,
               layer4=layer.level3_layer4,
               layer5=layer.level3_layer5,
               layer6=layer.level3_layer6,
               layer7=layer.level3_layer7,
               ambient_sound=pygame.mixer.Sound(
                   os.path.join(
                       ".", "assets", "sounds", "level3_ambient.ogg"))
               )
