from dataclasses import dataclass, field
from typing import List
import enemies
import layer
# import random


@dataclass
class Level:
    name: str
    x: int = 0
    y: int = 0
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
    current_wave_enemies: List[enemies.Enemy] = field(default_factory=list)

    def generate_wave(self):
        pass

    def get_layers_list(self):
        return [self.layer0, self.layer1, self.layer2, self.layer3, self.layer4, self.layer5, self.layer6, self.layer7]


level0 = Level("Church",
               layer0=layer.level0_layer0,
               layer1=layer.level0_layer1)
level1 = Level("Fields",
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
               layer7=layer.level3_layer7)