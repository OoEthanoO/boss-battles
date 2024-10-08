import pytest

from boss_battles.character import Squirrel, Player, Stats
from boss_battles.game import BossBattle
from boss_battles.ability import Ability


class GameRunner:
    def __init__(self, battle: BossBattle):
        self.battle = battle
        self.log = ""
    
    def play(self, all_player_actions: list[list[tuple[str, str]]]):         
        while self.battle.next_round() and len(all_player_actions[0]) > 0:
            op_tokens = self.battle.get_opportunity_tokens()

            # get player actions
            actions = []
            for i, player in enumerate(self.battle.players):
                this_player_actions = all_player_actions[i]
                action, target, solve_token = this_player_actions.pop(0)
                boss = self.battle._bosses.get(target)
                actions.append((player, action, boss, solve_token))

            self.log += self.battle.players_turn(actions)
            
            # boss actions
            self.log += self.battle.bosses_turn()
        
        return self.log


class TestAttack(Ability):
    identifier = "testattack"
    name = "Test Attack"
    effect = Stats(health=-1)
    cost = Stats(stamina=-1)

    def algorithm(self, op_token):
        return ""

    def verify(self, op_token, solve_token):
        # Bite is always castable
        return True


class DifficultTestAttack(Ability):
    identifier = "difficulttestattack"
    name = "Difficult Test Attack"
    effect = Stats(health=-1)
    cost = Stats(stamina=-1)

    def algorithm(self, op_token):
        return "correcttoken"


def test_squirrel_battle():

    boss = Squirrel()
    player = Player("tester")
    battle = BossBattle(players=[player], bosses=[boss])
    runner = GameRunner(battle)

    player._stats.health = 100
    boss._stats.health = 200
    boss._ability_set = ("testattack", )
    all_player_actions = [
        [('testattack', 'squirrel', 'solvetoken')],
    ]
    runner.play(all_player_actions)
    assert boss._stats.health == 199
    assert player._stats.health == 99


def test_squirrel_battle_taking_correct_solves_into_account():
    boss = Squirrel()
    player = Player("tester")
    battle = BossBattle(players=[player], bosses=[boss])
    runner = GameRunner(battle)

    player._stats.health = 100
    boss._stats.health = 200
    boss._ability_set = ("testattack", )
    all_player_actions = [
        [('difficulttestattack', 'squirrel', 'wrongsolvetoken')],
    ]
    log = runner.play(all_player_actions)
    assert boss._stats.health == 200
    assert "tester: wrong solve token!" in log.lower()

    all_player_actions = [
        [('difficulttestattack', 'squirrel', 'correcttoken')],
    ]

    log = runner.play(all_player_actions)
    assert boss._stats.health == 199
    assert "tester used difficult test attack on squirrel" in log.lower()


# def test_squirrel_battle_taking_op_tokens_into_account():