

from typing import Protocol, Optional
from collections import deque
import time



class Connection(Protocol):
    def send(self, data: str) -> None: ...
    
    def receive(self) -> str: ...
    
    def receive_full(self) -> tuple[bytes, int, int]: ...



class FakeRadio:
    _groups: dict[int, list['FakeRadio']] = {}

    @staticmethod
    def add_to_group(group: int, radio: 'FakeRadio') -> None:
        try:
            FakeRadio._groups[group].append(radio)
        except KeyError:
            FakeRadio._groups[group] = [radio]

    def __init__(self, group: int = 0, cache_size: int = 3) -> None:
        self._message_queue = deque(maxlen=cache_size)
        self._group = group
        FakeRadio.add_to_group(self._group, self)

    def send(self, message: str) -> None:
        for group in FakeRadio._groups.keys():
            for radio in FakeRadio._groups[group]:
                if radio == self:
                    continue
                radio._add_message_to_queue(message)
            
    def receive(self) -> Optional[str]:
        try:
            return self._message_queue.popleft()[0]
        except IndexError:
            return None
    
    def receive_full(self) -> Optional[tuple[str, int, int]]:
        try:
            return self._message_queue.popleft()
        except IndexError:
            return None
        
    def _add_message_to_queue(self, message: str) -> None:
        timestamp = int(time.time() * 1000)
        rssi = 0
        self._message_queue.append((message, rssi, timestamp))


