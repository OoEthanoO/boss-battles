import pytest


from boss_battles.game import BossBattle
from boss_battles.character import Squirrel, Player


def test_can_create_new_battle():
    battle = BossBattle(players=[Player("mrgallo"), Player("dave")], bosses=[Squirrel()])
    assert len(battle._players) == 2
    assert len(battle._bosses) == 1


def test_players_and_bosses_correctly_indexed():
    player_one = Player("mrgallo")
    player_two = Player("dave")
    boss = Squirrel()
    battle = BossBattle(players=[player_one, player_two], bosses=[boss])
    assert battle._players["mrgallo"] is player_one
    assert battle._players["dave"] is player_two
    assert battle._bosses["squirrel"] is boss

def test_multiple_bosses_of_same_type_have_unique_names():
    b1 = Squirrel()
    b2 = Squirrel()
    b3 = Squirrel()
    battle = BossBattle(players=[], bosses=[b1, b2, b3])

    assert len(battle._bosses) == 3
    assert battle._bosses["squirrel1"] is b1
    assert battle._bosses["squirrel2"] is b2
    assert battle._bosses["squirrel3"] is b3

    assert type(battle._bosses["squirrel1"]) is Squirrel