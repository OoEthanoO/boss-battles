from .fake_radio import FakeRadio, Connection


class Game:
    def __init__(self, radio: Connection):
        self.radio = radio

    def run(self):
        print("running game")

