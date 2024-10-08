import pytest

from boss_battles.game_server import GameServer


class FakeReader:
    def __init__(self):
        self.messages = []

    def add_message(self, msg: str):
        self.messages.append(msg)

    def add_messages(self, messages: list[str]):
        self.messages += messages

    def read(self) -> list[str]:
        tmp = self.messages
        self.messages = []
        return tmp
    

def test_game_server_can_store_incoming_messages():
    reader = FakeReader()
    reader.add_messages([
        "one",
        "two"
    ])
    game_server = GameServer(reader=reader, testing=True)
    # in lieu of game_server.run()
    game_server.get_messages()
    assert len(game_server.messages) == 2
    
    game_server.current_phase()
    assert len(game_server.messages) == 0, "Handled messages get cleared from the messages queue"


def test_game_server_registers_users():
    reader = FakeReader()
    reader.add_messages([
        "user1/register",
        "user2/register"
    ])
    game_server = GameServer(reader=reader, testing=True)
    game_server.run()
    assert len(game_server.messages) == 0, "Handled messages get cleared"
    assert len(game_server.registered_usernames) == 2


def test_game_server_registers_users_who_register_properly():
    reader = FakeReader()
    reader.add_messages([
        "user1/register",
        "user2/bad_command",
        "bad_command",
        "user2/register"
    ])
    game_server = GameServer(reader=reader, testing=True)
    game_server.run()
    assert len(game_server.registered_usernames) == 2


def test_game_server_registers_only_unique_names_case_insensitive():
    reader = FakeReader()
    reader.add_messages([
        "user1/register",
        "user2/register",
        "usER2/register",
        "USER2/register",
    ])
    game_server = GameServer(reader=reader, testing=True)
    game_server.run()
    assert len(game_server.registered_usernames) == 2


def test_game_server_changes_to_battle_phase_when_registering_done():
    reader = FakeReader()
    reader.add_messages([
        "user1/register",
        "done"
    ])
    game_server = GameServer(reader=reader, testing=True)
    game_server.run()
    assert game_server.current_phase == game_server.battle

