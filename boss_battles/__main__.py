from .game import Game
from.fake_radio import FakeRadio


fake_radio = FakeRadio()
Game(radio=fake_radio).run()