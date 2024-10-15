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
        self.ser = None  # Serial connection initialized to None

    def open(self):
        """Open the serial connection."""
        self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)

    def close(self):
        """Close the serial connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()

    def read(self) -> list[str]:
        messages = []
        while self.ser.in_waiting > 0:
            message = self.ser.readline().decode('utf-8').strip()
            messages.append(message)
            print(f"received: {message}")
        return messages


class GameServer:
    def __init__(self, bosses: list[Boss], reader: Optional[Reader] = None, testing: bool = False):
        self._bosses = bosses
        self._testing = testing
        if reader is None:
            reader = SerialReader()
        self._reader = reader
        self._action_strings = []
        self._registered_usernames = set()
        self._current_phase = self._registration_phase
        self._battle = None
    
    @property
    def battle(self) -> BossBattle:
        return self._battle
    
    def run(self):
        self._reader.open()
        try:
            while True:
                self._get_messages()
                self._current_phase()

                if self._testing is True:
                    break
        except KeyboardInterrupt:
            pass

        self._reader.close()

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
        if self._battle.next_round():
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
            

            #TODO: There needs to be some sort of delay here to allow
            #      players to make their move. Then, player actions will be accounted for
            #      If a target dies before their action is registered, they lose the turn.
            #      This should allow for more coordination between players.
            #      Or should players be able to wait to see other's effects? Eventually the game pace will be
            #      too fast for this and their microbits will have to act for the players.

            for command in valid_commands:
                result = self._battle.handle_action(command)
                print(result)

            # TODO: There should be a countdown timer after the player actions and before the boss acts.

            # boss action
            result = self._battle.bosses_turn()
            print(result)
