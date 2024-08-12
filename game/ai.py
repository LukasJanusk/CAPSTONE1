from dataclasses import dataclass
from abc import ABC, abstractmethod
import random
import pygame
from game import enemies
from game import player


@dataclass
class AI(ABC):

    @abstractmethod
    def choose_action():
        pass


@dataclass
class DemonAI(AI):
    @staticmethod
    def choose_action(demon: enemies.Demon, player: player.Player):
        current_time = pygame.time.get_ticks()
        if current_time - demon.action_last_update > demon.action_duration:
            demon.action_last_update = current_time
            choice = random.choice(demon.actions)
            if choice == "seek":
                DemonAI.seek(demon, player)
            elif choice == "flee":
                DemonAI.flee(demon, player)
            elif choice == "idle":
                DemonAI.idle(demon, player)
            else:
                demon.idle = True

    @staticmethod
    def seek(demon: enemies.Demon, player: player.Player):
        demon.action_duration = 1000
        if not demon.dead and not demon.spawn:
            if int(demon.x + 250) in range(
                    int(player.x + 62) - 150,
                    int(player.x + 62) + 150
                    ):
                demon.attacking = True
                demon.running = False
            elif (player.x + 62) <= (demon.x + 250):
                demon.facing_right = False
                demon.running = True
            elif (player.x + 62) > (demon.x + 250):
                demon.facing_right = True
                demon.running = True

    @staticmethod
    def flee(demon: enemies.Demon, player: player.Player):
        demon.action_duration = 500
        if not demon.dead and not demon.attacking and not demon.spawn:
            demon.running = True
            if player.x > demon.x:
                demon.facing_right = False
            else:
                demon.facing_right = False

    @staticmethod
    def idle(demon: enemies.Demon, player: player.Player):
        demon.action_duration = 500
        if not demon.dead and not demon.attacking and not demon.spawn:
            if demon.x in range(player.x - 501, player.x + 600):
                demon.idle = True
            else:
                demon.running = True
                if player.x < demon.x:
                    demon.facing_right = False
                else:
                    demon.facing_right = True


@dataclass
class ImpAI(AI):
    @staticmethod
    def choose_action(imp: enemies.Imp, player: player.Player):
        current_time = pygame.time.get_ticks()
        if current_time - imp.action_last_update > imp.action_duration:
            imp.action_last_update = current_time
            choice = random.choice(imp.actions)
            if choice == "seek":
                ImpAI.seek(imp, player)
            elif choice == "flee":
                ImpAI.flee(imp, player)
            elif choice == "idle":
                ImpAI.idle(imp, player)
            else:
                imp.idle = True

    @staticmethod
    def seek(imp: enemies.Imp, player: player.Player):
        imp.action_duration = 500
        if not imp.dead and not imp.spawn:
            if imp.x - 50 >= player.x:
                imp.facing_right = False
                imp.attacking = True
                imp.running = True
            elif imp.x < player.x + 30:
                imp.facing_right = True
                imp.attacking = True
                imp.running = True
            else:
                imp.idle = True

    @staticmethod
    def flee(imp: enemies.Imp, player: player.Player):
        imp.action_duration = 500
        if not imp.dead and not imp.spawn:
            if imp.x >= player.x:
                imp.attacking = False
                imp.running = True
                imp.facing_right = True
            elif imp.x < player.x:
                imp.attacking = False
                imp.running = True
                imp.facing_right = False

    def idle(imp: enemies.Imp, player: player.Player):
        if not imp.spawn:
            imp.action_duration = 1500
            imp.running = False
            imp.idle = True
