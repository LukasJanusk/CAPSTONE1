import re
import json
import pygame
from dataclasses import dataclass
import os


@dataclass
class Typing_Controller():
    user_text: str = ""
    typing: bool = True
    typo: bool = False
    last_update = pygame.time.get_ticks()

    def get_user_input(self, event: pygame.event.Event):
        if self.typing is True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.typing = False
                    return self.user_text
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode


@dataclass
class User:
    NAME: str
    level0: bool = True
    level1: bool = True
    level2: bool = True
    level3: bool = True
    level4: bool = True
    level5: bool = True
    _level0_highscore: int = 0
    _level1_highscore: int = 0
    _level2_highscore: int = 0
    _level3_highscore: int = 0
    _level4_highscore: int = 0
    _level5_highscore: int = 0
    input_manager = Typing_Controller()

    def __str__(self) -> str:
        return f"{self.NAME}"

    @property
    def NAME(self) -> str:
        return self._NAME

    @NAME.setter
    def NAME(self, name: str):
        regex = r"[a-zA-Z0-9]+(?: [a-zA-Z0-9]+)*"
        if not re.match(regex, name):
            raise ValueError("NAMES MUST BE LETTERS AND NUMBERS ONLY")
        else:
            self._NAME = name

    @property
    def level1_highscore(self) -> int:
        return self._level1_highscore

    @ level1_highscore.setter
    def level1_highscore(self, value):
        if value > self._level1_highscore:
            self._level1_highscore = value

    @property
    def level2_highscore(self) -> int:
        return self._level1_highscore

    @ level2_highscore.setter
    def level2_highscore(self, value):
        if value > self._level2_highscore:
            self._level2_highscore = value

    @property
    def level3_highscore(self) -> int:
        return self._level3_highscore

    @ level3_highscore.setter
    def level3_highscore(self, value):
        if value > self._level4_highscore:
            self._level3_highscore = value

    @property
    def level4_highscore(self) -> int:
        return self._level4_highscore

    @ level4_highscore.setter
    def level4_highscore(self, value):
        if value > self._level4_highscore:
            self._level4_highscore = value

    @property
    def level5_highscore(self) -> int:
        return self._level5_highscore

    @ level5_highscore.setter
    def level5_highscore(self, value):
        if value > self._level5_highscore:
            self._level5_highscore = value

    def to_dict(self) -> dict:
        return {"user": [{"NAME": self.NAME},
                         {"level0": self.level0},
                         {"level1": self.level1},
                         {"level2": self.level2},
                         {"level3": self.level3},
                         {"level4": self.level4},
                         {"level5": self.level5},
                         {"level0_highscore": self.level0_highscore},
                         {"level1_highscore": self.level1_highscore},
                         {"level2_highscore": self.level2_highscore},
                         {"level3_highscore": self.level3_highscore},
                         {"level4_highscore": self.level4_highscore},
                         {"level5_highscore": self.level5_highscore}]}

    def save_user(self) -> bool:
        data = self.to_dict()
        try:
            with open(os.path.join(".", "user", "user.json"), mode="w") as file:
                json.dump(data, file, indent=4)
                print("User data saved")
                return True
        except Exception as e:
            print(f"Failed to save user data: {e}")
            return False

    def load_user(self) -> bool:
        file_path = os.path.join(".", "user", "user.json")
        if not os.path.isfile(file_path):
            self.save_user()
        else:
            try:
                path = os.path.join(".", "user", "user.json")
                with open(path, mode="r") as file:
                    data = json.load(file)
                    self.NAME = data["user"][0]["NAME"]
                    self.level0 = data["user"][1]["level0"]
                    self.level1 = data["user"][2]["level1"]
                    self.level2 = data["user"][3]["level2"]
                    self.level3 = data["user"][4]["level3"]
                    self.level4 = data["user"][5]["level4"]
                    self.level5 = data["user"][6]["level5"]
                    self.level0_highscore = data["user"][7]["level0_highscore"]
                    self.level1_highscore = data["user"][8]["level1_highscore"]
                    self.level2_highscore = data["user"][9]["level2_highscore"]
                    self.level3_highscore = data["user"][10]["level3_highscore"]
                    self.level4_highscore = data["user"][11]["level4_highscore"]
                    self.level5_highscore = data["user"][12]["level5_highscore"]
                    self.input_manager = Typing_Controller()
                    print("User data loaded")
                    return True
            except Exception as e:
                print(f"Failed to load user data: {e}")
                return False

    def reset_user_data(self):
        pass
