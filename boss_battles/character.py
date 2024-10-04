from typing import Protocol, TYPE_CHECKING
from dataclasses import dataclass
import random


if TYPE_CHECKING:
    from .game import BossBattle
    from .ability import Ability
    from .character import Character

# caster, ability identifier, target
Action = tuple['Character', str, 'Character']

@dataclass
class Stats:
    health: int = 0
    mana: int = 0
    stamina: int = 0
    intelligence: int = 0
    agility: int = 0
    strength: int = 0


class Character(Protocol):
    _name: str
    _base_stats: Stats
    _stats: Stats


class Player:
    _name: str
    _base_stats: Stats
    _stats: Stats

    def __init__(self, name: str):
        self._name = name.lower()
        self._base_stats = Stats(50, 10, 10, 10, 10, 10)
        self._stats =      Stats(50, 10, 10, 10, 10, 10)


class Boss:
    _name: str
    _stats: Stats
    _ability_set: tuple[str]
    _opportunity_tokens: list[str]
    _opportunity_token_length: int = 4

    def __init__(self):
        # TODO: enforce restrintion on name (only alphanum)
        self._opportunity_tokens = []

    def is_alive(self):
        return self._stats.health > 0
    
    def get_opportunity_token(self) -> str:
        "Each boss will have random opportunity token generated each round"
        return self._opportunity_tokens[-1]
    
    def generate_opportunity_token(self):
        characters = "abcedfghijkmnpqrstuvwxyz0123456789"
        self._opportunity_tokens.append(''.join(random.choice(characters) for _ in range(self._opportunity_token_length)).lower())

    def do_turn(self, battle: 'BossBattle') -> Action:
        """
        The idea is every boss requests to do an 
        action to a target(s) and returns that request in the form of an Action tuple
        """
        raise NotImplementedError("Bosses must override the do_turn method.")


class Squirrel(Boss):
    _name: str = "squirrel"
    _base_stats: Stats = Stats(health=5, mana=0, stamina=5, intelligence=1, agility=100, strength=1)
    _stats     : Stats = Stats(health=5, mana=0, stamina=5, intelligence=1, agility=100, strength=1)
    _ability_set = ("bite", "cower")

    def do_turn(self, battle: 'BossBattle') -> Action:
        ability = random.choice(self._ability_set)
        random_player = random.choice(tuple(battle.players))
        return (self, ability, random_player)


class PracticeDummy(Boss):
    _name: str = "dummy"
    _stats: Stats = Stats(health=500)
    _base_stats: Stats = Stats(health=500)

    def do_turn(self, battle: 'BossBattle') -> Action:
        # self-heal increasing health pool by 2x the damage deficit (if any)
        if self._stats.health < 0:
            deficit = -self._stats.health
            increase = deficit // 2
            self._base_stats.health += increase
        self._stats.health = self._base_stats.health