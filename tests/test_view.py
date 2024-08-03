import pytest
import pygame
from ..game import view


def test_view_center_correct():
    surface1 = pygame.Surface((800, 100))
    surface2 = pygame.Surface((100, 100))
    result1 = view.View.center(surface1, surface2)
    assert result1 == 450
