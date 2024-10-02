from typing import Any, Optional

from .message import Message
from .character import Character


class BossBattle:
    def __init__(self, players: list[Character], bosses: list[Character]):
        # TODO: need a check to ensure all players and bosses have a unique name, or give them one like boss1, boss2.
        
        # Dictionary indexed by player name
        self._players = {p._name: p for p in players}

        # self._all_player_names: set[str] = set(p._name for p in players)

        # Dictionary indexed by boss name
        self._bosses = {b._name: b for b in bosses}

        # self._all_character_names: set[str] = set(b._name for b in bosses) | self._all_player_names
        self._round_count = 0
    
    def next_round(self) -> bool:
        if not self._should_continue():
            return False
        
        self._round_count += 1
        for boss in self._bosses.values():
            boss.generate_opportunity_token()
        
        return True
    
    def get_round(self) -> int:
        return self._round_count
    
    def _should_continue(self) -> bool:
        if len(BossBattle._filter_active(self._bosses.values())) < 1:
            return False

        if len(BossBattle._filter_active(self._players.values())) < 1:
            return False
        
        return True
        
    @staticmethod
    def _filter_active(characters: list[Character]) -> list[Character]:
        return [c for c in characters if c._stats.health > 0]


    def get_opportunity_tokens(self) -> list[str]:
        return [b._name + ":" + b.get_opportunity_token() for b in self._bosses.values()]

            
    def handle_action(self, action: Message) -> str:
        # TODO: should This be here or just raise error when we try to apply the action?
        # if not self._player_is_registered(m.user):
        #     # TODO: problem: fails silently, possible to collect all invalid and print at the end? 
        #     #       Or as it goes?
        #     continue

        # if not self._target_is_registered(m.target):
        #     continue

        return self._apply_action(m)


    def _player_is_registered(self, name: str) -> bool:
        return name in self._players.keys()


    def _target_is_registered(self, name: str) -> bool:
        return name in self._bosses.keys()


    def _apply_action(self, m: Message) -> str:
        player = self._players[m.user]
        target = self._bosses[m.target]
        # ability = 

        return "{player} {action} {target}"
    
