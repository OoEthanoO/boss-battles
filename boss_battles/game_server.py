import serial
from typing import Protocol, Optional

from .character import Boss, Player
from .game import BossBattle
from .utils import print_health_list, print_health_bar
from .command import InvalidActionStringError, Command


class Reader(Protocol):
    def read(self) -> list[str]:
        pass


class SerialReader:
    def __init__(self, port: str = "COM3", baud_rate: int = 115200):
        self.port = port
        self.baud_rate = baud_rate

    def read(self) -> list[str]:
        with serial.Serial(self.port, self.baud_rate) as ser:
            messages = []
            while ser.in_wating > 0:
                message = ser.readline().decode('utf-8').strip()
                messages.append(message)
        return messages


class GameServer:
    def __init__(self, bosses: list[Boss], reader: Optional[Reader] = None, testing: bool = False):
        self._bosses = bosses
        self._reader = reader
        self._testing = testing
        if reader is None:
            reader = SerialReader()
        self._action_strings = []
        self._registered_usernames = set()
        self._current_phase = self._registration_phase
        self._battle = None
    
    @property
    def battle(self) -> BossBattle:
        return self._battle
    
    def run(self):
        while True:
            self._get_messages()
            self._current_phase()

            if self._testing is True:
                break

    def _get_messages(self):
        self._action_strings += self._reader.read()

    def _registration_phase(self):
        message_queue = self._action_strings
        self._action_strings = []
        for message in message_queue:
            if message.lower() == "done":
                players = [Player(n) for n in self._registered_usernames]
                self._battle = BossBattle(bosses=self._bosses, players=players)
                self._current_phase = self._battle_phase
                return
            
            try:
                user, command = message.split("/")
            except ValueError:
                continue

            if command.lower() != "register":
                continue

            user = user.lower()
            if user in self._registered_usernames:
                print("Error: " + user + " already added.")
                continue

            self._registered_usernames.add(user)
            print("Welcome " + user.upper() + "!")
    
    def _battle_phase(self):
        while self._battle.next_round():
            print("=" * 10 + " ROUND " + str(self._battle.get_round()) + " " + "=" * 10)
            print_health_list("BOSSES", self._battle._bosses.values())
            print_health_list("PLAYERS", self._battle._players.values())
            print()

            opportunity_tokens = self._battle.get_opportunity_tokens()
            print(f"OPPORTUNITY TOKEN{'S' if len(opportunity_tokens) > 1 else ''}")
            for token in opportunity_tokens:
                print(token)
            print()

            # get actions from players

            valid_commands = []
            for action in self._action_strings:
                try:
                    command = Command(action)
                except InvalidActionStringError as e:
                    print(f"Invalid message: '{action}'")

                if not any(c.user == command.user for c in valid_commands):
                    valid_commands.append(command)
            
            for command in valid_commands:
                result = self._battle.handle_action(command)
                print(result)

            # boss action
            result = self._battle.bosses_turn()
            print(result)

            if self._testing is True:
                break
