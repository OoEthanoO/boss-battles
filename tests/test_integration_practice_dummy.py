import pytest

from boss_battles.game import BossBattle
from boss_battles.character import Player, PracticeDummy, Stats
from boss_battles.command import Command
from boss_battles.ability import AbilityRegistry, Ability


def test_practice_dummy_battle():
    boss = PracticeDummy()
    player = Player("player")
    battle = BossBattle(players=[player], bosses=[boss])

    assert boss._stats.health == 500

    # PLAYER TURN
    message = Command("player@dummy/attack")
    battle.handle_action(message)

    # Confirm the attack was made on the boss
    ability = AbilityRegistry.registry.get("attack")
    assert ability.identifier == "attack"

    ability_damage = -ability.effect.health
    assert boss._stats.health == 500 - ability_damage

    # BOSS TURN
    boss.do_turn(battle)

    # the practice dummy restores whatever damage it took
    assert boss._stats.health == 500


def test_practice_dummy_health_expands_when_damaged_beyond_capacity():
    class MonsterTestAttack(Ability):
        identifier = "monstertest"
        name = "Monster Test Attack"
        effect = Stats(health=-1000)
        cost = Stats()

    boss = PracticeDummy()
    player = Player("player")
    battle = BossBattle(players=[player], bosses=[boss])

    assert boss._stats.health == 500

    # PLAYER TURN
    message = Command("player@dummy/monstertest")
    battle.handle_action(message)

    monster_damage = -MonsterTestAttack.effect.health
    assert boss._stats.health == 500 - monster_damage

    # BOSS TURN
    boss.do_turn(battle)

    # Dummy should add x2 the damage deficit caused by the last round
    # 500 - 1000 = -500
    # so it should add 250 hp to base stats
    assert boss._base_stats.health == 500 + 250
    assert boss._stats.health == 500 + 250

