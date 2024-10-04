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
    a = Stats(0, 1, 2, 3, 4, 5)
    b = Stats(10, 20, 30, 40, 50, 60)

    a += b
    assert a.health == 10
    assert a.mana == 21
    assert a.stamina == 32
    assert a.intelligence == 43
    assert a.agility == 54
    assert a.strength == 65
