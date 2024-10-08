import serial
from typing import Protocol, Optional


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
    def __init__(self, reader: Optional[Reader] = None, testing: bool = False):
        self.messages = []
        self.current_phase = self.register_users
        if reader is None:
            reader = SerialReader()
        self.reader = reader
        self.testing = testing
        self.registered_usernames = set()
    
    def run(self):
        while True:
            self.get_messages()
            self.current_phase()

            if self.testing is True:
                break

    def get_messages(self):
        self.messages += self.reader.read()

    def register_users(self):
        message_queue = self.messages
        self.messages = []
        for message in message_queue:
            if message.lower() == "done":
                self.current_phase = self.battle
                return
            
            try:
                user, command = message.split("/")
            except ValueError:
                continue

            if command.lower() != "register":
                continue

            user = user.lower()
            if user in self.registered_usernames:
                print("Error: " + user + " already added.")
                continue

            self.registered_usernames.add(user)
            print("Welcome " + user.upper() + "!")
    
    def battle(self):
        pass