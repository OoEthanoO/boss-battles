from microbit import *
import radio


from .game import GameRunner

game = GameRunner(radio)
game.register_users()