from typing import Protocol
from dataclasses import dataclass
import random


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


class Squirrel(Boss):
    _name: str = "squirrel"
    _base_stats: Stats = Stats(health=5, mana=0, stamina=5, intelligence=1, agility=100, strength=1)
    _stats: Stats =      Stats(health=5, mana=0, stamina=5, intelligence=1, agility=100, strength=1)
