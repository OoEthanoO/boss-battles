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



