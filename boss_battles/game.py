from dataclasses import dataclass
from typing import Any, Protocol


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
        self._name = name
        self._base_stats = Stats(50, 10, 10, 10, 10, 10)
        self._stats =      Stats(50, 10, 10, 10, 10, 10)


class Boss:
    _name: str
    _stats: Stats

    def is_alive(self):
        return self._stats.health > 0
    

class Squirrel(Boss):
    _name: str = "Squirrel"
    _base_stats: Stats = Stats(health=5, mana=0, stamina=5, intelligence=1, agility=100, strength=1)
    _stats: Stats =      Stats(health=5, mana=0, stamina=5, intelligence=1, agility=100, strength=1)


class BossBattle:
    def __init__(self, players: list[dict[str, Any]], bosses: list[Boss]):
        self._players = players
        self._bosses = bosses

    def run(self):
        print("Running game")
        print(f"Boss{'es' if len(self._bosses) > 1 else ''}: {', '.join(map(str.upper, [b._name for b in self._bosses]))}")
        print()
        print("Players:\n" + "\n".join(map(str.upper, [p._name for p in self._players])))
        while self._should_continue_game():
            for b in self._bosses:
                BossBattle._print_health_bar(b)
    
    def _should_continue_game(self):
        if len(BossBattle._filter_active(self._bosses)) < 1:
            return False

        if len(BossBattle._filter_active(self._players)) < 1:
            return False
        
        return True
        
    @staticmethod
    def _filter_active(characters: list[Character]) -> list[Character]:
        return [c for c in characters if c._stats.health > 0]

    @staticmethod
    def _print_health_bar(character: Character):
        pass

