import model
import view


class Controller:
    def __init__(self):
        self.model = model.Model()
        self.view = view.View()

    def get_layers(self):
        