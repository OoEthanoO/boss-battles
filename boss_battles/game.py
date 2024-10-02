from typing import Any, Optional

from .message import Message
from .character import Character


class BossBattle:
    def __init__(self, players: list[Character], bosses: list[Character]):
        self._players = players
        self._bosses = bosses
        # TODO: need a check to ensure all bosses have a unique name, or give them one like boss1, boss2.
        self._round_count = 0
    
    def next_round(self) -> bool:
        if not self._should_continue():
            return False
        
        self._round_count += 1
        for boss in self._bosses:
            boss.generate_opportunity_token()
        
        return True
    
    def get_round(self) -> int:
        return self._round_count
    
    def _should_continue(self) -> bool:
        if len(BossBattle._filter_active(self._bosses)) < 1:
            return False

        if len(BossBattle._filter_active(self._players)) < 1:
            return False
        
        return True
        
    @staticmethod
    def _filter_active(characters: list[Character]) -> list[Character]:
        return [c for c in characters if c._stats.health > 0]


    def get_opportunity_tokens(self) -> list[str]:
        return [b._name + ":" + b.get_opportunity_token() for b in self._bosses]

    
    def handle_actions(self, messages: list[Message]) -> None:
        for m in messages:
            print("{} {} {} {}".format(m.user, m.target, m.action, m.args))

