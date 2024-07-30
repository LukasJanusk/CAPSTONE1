from dataclasses import dataclass
import enemies
import layer
import random


@dataclass
class Level:
    name: str
    x: int
    y: int
    layer0: layer.Layer = None
    layer1: layer.Layer = None
    layer2: layer.Layer = None
    layer3: layer.Layer = None
    layer4: layer.Layer = None
    layer5: layer.Layer = None
    layer6: layer.Layer = None
    layer7: layer.Layer = None
    waves: int = 10
    current_wave: int = 0
    current_wave_enemies = []

    def generate_wave(self):
        pass

    def get_layers_list(self):
        return [self.layer0, self.layer1, self.layer2, self.layer3, self.layer4, self.layer5, self.layer6, self.layer7]
