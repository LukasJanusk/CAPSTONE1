import pygame
from game import view
import os
import sys


def pytest_configure(config):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(root_dir)
    sys.path.append(root_dir)


def test_view_center_correct():
    surface1 = pygame.Surface((800, 100))
    surface2 = pygame.Surface((100, 100))
    result1 = view.View.center(surface1, surface2)
    assert result1 == 350
    surface3 = pygame.Surface((1000, 100))
    surface4 = pygame.Surface((600, 100))
    result2 = view.View.center(surface3, surface4)
    assert result2 == 200
