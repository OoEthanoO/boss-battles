from .game import BossBattle, Squirrel, Player


bosses = [
    Squirrel()
]

players = [
    Player("Mr. Gallo")
]

BossBattle(players=players, bosses=bosses).run()