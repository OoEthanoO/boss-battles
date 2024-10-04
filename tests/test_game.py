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

    # ensure it removed the reference to the first squirrel
    assert battle._bosses.get("squirrel", False) is False

    # test that the object's name was also changed, not just
    # the reference in the dict
    assert b1._name == "squirrel1"


def test_should_continue_returns_false_with_one_character_per_team():
    p = Player("player")
    b = Squirrel()
    battle = BossBattle(players=[p], bosses=[b])
    
    assert battle._should_continue() == True

    b._stats.health = 0
    assert battle._should_continue() == False

    p._stats.health = 0
    assert battle._should_continue() == False

    b._stats.health = 100
    assert battle._should_continue() == False


def test_should_get_opportunity_tokens_for_all_bosses():
    b1 = Squirrel()
    b2 = Squirrel()
    b3 = Squirrel()
    p = Player("test")
    battle = BossBattle(players=[p], bosses=[b1, b2, b3])

    # need to generate tokens first
    with pytest.raises(IndexError):
        battle.get_opportunity_tokens()

    battle.next_round()
    tokens = battle.get_opportunity_tokens()
    assert len(tokens) == 3

    boss_names = tuple(t.split(":")[0] for t in tokens)
    assert "squirrel1" in boss_names
    assert "squirrel2" in boss_names
    assert "squirrel3" in boss_names

    unique_tokens = set(t.split(":")[1] for t in tokens)
    assert len(unique_tokens) == 3, "should fail VERY rarely due to RNG"
