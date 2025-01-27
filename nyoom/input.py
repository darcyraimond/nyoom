from .component import Component

class Input(Component):

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __hash__(self):
        return hash(self.name)