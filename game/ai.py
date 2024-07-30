import enemies
from player import char


class AI:
    def __init__(self, name, enemy):
        self.name: str = name
        self.enemy: enemies.Enemy = enemy
        self.player = char

    def seek(self):
        if self.enemy.x + 20 <= self.player.x and self.player.x <= self.enemy.x + self.enemy.hitbox_width:
            self.enemy.attacking = True
            self.enemy.running = False
        elif self.enemy.exist is True and self.enemy.dead is False and self.enemy.attacking is False:
            if self.enemy.x > self.player.x + 30:
                self.enemy.running = True
                self.enemy.facing_right = False
            elif self.enemy.x < self.player.x - 30:
                self.enemy.running = True
                self.enemy.facing_right = True
        else:
            self.enemy.idle = True
