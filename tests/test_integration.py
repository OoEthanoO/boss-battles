import pytest
from unittest.mock import patch

from boss_battles.character import Squirrel, Player, Stats
from boss_battles.game import BossBattle
from boss_battles.ability import Ability, EffectType
from boss_battles.game_server import GameServer
from helpers import FakeReader


# class GameRunner:
#     def __init__(self, battle: BossBattle):
#         self.battle = battle
#         self.log = ""
    
#     def play(self, all_player_actions: list[list[tuple[str, str]]]):         
#         while self.battle.next_round() and len(all_player_actions[0]) > 0:
#             op_tokens = self.battle.get_opportunity_tokens()

#             # get player actions
#             actions = []
#             for i, player in enumerate(self.battle.players):
#                 this_player_actions = all_player_actions[i]
#                 action, target, solve_token = this_player_actions.pop(0)
#                 boss = self.battle._bosses.get(target)
#                 actions.append((player, action, boss, solve_token))

#             self.log += self.battle.players_turn(actions)
            
#             # boss actions
#             self.log += self.battle.bosses_turn()
        
#         return self.log


class TestAttack(Ability):
    identifier = "testattack"
    name = "Test Attack"
    effect_type = EffectType.BLUDGEONING
    effect_die = (1, 1)
    modifier_type = Stats.Type.STRENGTH

    def algorithm(self, op_token):
        return ""

    def verify(self, op_token, solve_token):
        # Bite is always castable
        return True


class DifficultTestAttack(Ability):
    identifier = "difficulttestattack"
    name = "Difficult Test Attack"
    effect_type = EffectType.BLUDGEONING
    effect_die = (1, 1)
    modifier_type = Stats.Type.STRENGTH

    def algorithm(self, op_token):
        return "correcttoken"


# player: 20 roll 100% hit chance, two rolls of 1 give 2 damage
# boss:   20 roll 100% hit chance, two rolls of 1 give 2 damage
@patch("random.randint", side_effect=[20, 1, 1, 20, 1, 1])
def test_squirrel_battle(mock_randint):
    class OnlyBiteSquirrel(Squirrel):
        _ability_set = ("bite",)

    boss = OnlyBiteSquirrel()
    reader = FakeReader()
    reader.add_messages([
        "player/register",
        "done"
    ])
    runner = GameServer(bosses=[boss], reader=reader, testing=True)
    runner.run()
    assert len(runner.battle.players) == 1
    assert runner._current_phase == runner._battle_phase

    boss_health_before = boss._stats.health
    player = runner.battle.get_player('player')
    player_health_before = player._stats.health
    reader.add_message("player@squirrel/punch")
    runner.run()
    assert boss._stats.health == boss_health_before - 2
    assert player._stats.health == player_health_before - 2
    

@patch("random.randint", side_effect=[20, 1, 1])
def test_squirrel_battle_taking_correct_solves_into_account(mock_randint):
    boss = Squirrel()
    boss._stats.health = 2
    reader = FakeReader()
    reader.add_messages([
        "player/register",
        "done"
    ])
    runner = GameServer(bosses=[boss], reader=reader, testing=True)
    runner.run()

    boss_previous_health = boss._stats.health
    reader.add_message("player@squirrel/difficulttestattack wrongtoken")
    runner.run()
    assert boss._stats.health == boss_previous_health  # bad token, so ability doesn't trigger


# def test_squirrel_battle_taking_op_tokens_into_account():

# def test_cower_doesnt_inflict_damage():