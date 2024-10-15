import pytest


from boss_battles.character import Boss, Stats, Squirrel, Player
from boss_battles.game import BossBattle


def test_boss_do_turn_raises_not_implemented_error():
    class TestBoss(Boss):
        _name = "test"
        _base_stats = Stats()
        _stats = Stats()

    boss = TestBoss()
    
    with pytest.raises(NotImplementedError):
        boss.do_turn(BossBattle([], []))


def test_stats_add_together():
    a = Stats(
        health = 0,
        strength = 2,
        constitution = 3,
        dexterity = 4,
        wisdom = 5,
        charisma = 6,
        intelligence = 7
    )
    b = Stats(
        health = 10,
        strength = 30,
        constitution = 40,
        dexterity = 50,
        wisdom = 60,
        charisma = 70,
        intelligence = 80
    )

    a += b
    assert a.health == 10
    assert a.strength == 32
    assert a.constitution == 43
    assert a.dexterity == 54
    assert a.wisdom == 65
    assert a.charisma == 76
    assert a.intelligence == 87
