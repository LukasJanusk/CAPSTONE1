import os
import sys
import pytest
from game import user

user1 = user.User("Test")
user2 = user.User("TEST101")
user1.level0_highscore = 100
user2.level0_highscore = 10


def pytest_configure(config):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(root_dir)
    sys.path.append(root_dir)


def test_to_dict():
    result1 = user1.to_dict()
    assert result1 == {'user': [{'NAME': 'Test'},
                                {'level0': True},
                                {'level1': True},
                                {'level2': True},
                                {'level3': True},
                                {'level4': True},
                                {'level5': True},
                                {'level0_highscore': 100},
                                {'level1_highscore': 0},
                                {'level2_highscore': 0},
                                {'level3_highscore': 0},
                                {'level4_highscore': 0},
                                {'level5_highscore': 0}]}
    result2 = user2.to_dict()
    assert result2 == {'user': [{'NAME': 'TEST101'},
                                {'level0': True},
                                {'level1': True},
                                {'level2': True},
                                {'level3': True},
                                {'level4': True},
                                {'level5': True},
                                {'level0_highscore': 10},
                                {'level1_highscore': 0},
                                {'level2_highscore': 0},
                                {'level3_highscore': 0},
                                {'level4_highscore': 0},
                                {'level5_highscore': 0}]}


def test_user_name_errors():
    with pytest.raises(ValueError):
        user1.name = "#@@3$#@@$"
    with pytest.raises(ValueError):
        user1.name = "::::"
    with pytest.raises(TypeError):
        user1.name = {"asd": "32"}


def test_user_name_change():
    user1.name = "Mark"
    assert user1.name == "Mark"
    user1.name = "Test"


def test_highscore_change():
    user1.level0_highscore = 90
    assert user1.level0_highscore == 100
    user2.level0_highscore = 90
    assert user2.level0_highscore == 90
