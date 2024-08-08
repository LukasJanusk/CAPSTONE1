import os
import sys
import pygame
from game import attacks


hitbox1 = pygame.Rect(10, 10, 50, 50)
hitbox2 = pygame.Rect(50, 50, 500, 500)
hitbox3 = pygame.Rect(100, 100, 30, 30)
hitbox4 = pygame.Rect(-50, -50, 30, 30)
hitbox5 = pygame.Rect(500, 600, 1000, 1000)
hitbox6 = pygame.Rect(0, 0, 500, 500)

attack1 = attacks.Attack(None, 50, [1, 3, 5], 500, 500)
attack2 = attacks.Attack(None, 1, [4, 5, 6, 7, 8, 9], 50, 50)


def pytest_configure(config):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(root_dir)
    sys.path.append(root_dir)


def test_attacks_hit():
    result1 = attack1.hit(1, hitbox1)
    assert result1 == 50
    result2 = attack1.hit(0, hitbox1)
    assert result2 is False
    result3 = attack1.hit(1, hitbox5)
    assert result3 is False
    result4 = attack1.hit(3, hitbox1)
    assert result4 == 60
    result5 = attack1.hit(5, hitbox1)
    assert result5 == 70
    result6 = attack1.hit(5, hitbox4)
    assert result6 is False
    result7 = attack2.hit(5, hitbox2)
    assert result7 is False
    result8 = attack2.hit(4, hitbox1)
    assert result8 == 1
    result9 = attack2.hit(5, hitbox1)
    assert result9 == 1
    result10 = attack2.hit(9, hitbox1)
    assert result10 == 2


def test_update_hitbox():
    assert attack1.hitbox == hitbox6
    assert attack1.hitbox != hitbox2
    updated1 = attack1.update_hitbox(50, 50, True)
    assert updated1 != hitbox6
    assert updated1 == hitbox2

    assert attack2.hitbox != hitbox1
    updated2 = attack2.update_hitbox(10, 10, True)
    assert updated2 == hitbox1
