import pytest

from boss_battles.character import Squirrel, Player
from boss_battles.game import BossBattle


class GameRunner:
    def __init__(self, battle: BossBattle):
        self.battle = battle
    
    def play(self, num_rounds: int=1):
        while self.battle.next_round() and self.battle._round_count <= num_rounds:
            op_tokens = self.battle.get_opportunity_tokens()

            # get player actions
            for player in self.battle.players:
                assert type(player) is Player

            # for every player action:
            #     self.battle.handle_action()
            
            # boss actions
            self.battle.boss_turn()

def test_squirrel_battle():
    boss = Squirrel()
    player = Player("tester")
    battle = BossBattle(players=[player], bosses=[boss])
    runner = GameRunner(battle)

    player._stats.health = 100
    boss._ability_set = ("bite", )
    runner.play()
    assert player._stats.health < 100