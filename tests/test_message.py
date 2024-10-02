import pytest

from boss_battles.message import Message, InvalidMessageError


def test_valid_message_no_arguments():
    msg = Message("user123@target456/cmd")
    assert msg.user == "user123"
    assert msg.target == "target456"
    assert msg.action == "cmd"
    assert msg.args == []

def test_valid_message_with_arguments():
    msg = Message("user123@target456/cmd arg1 arg2")
    assert msg.user == "user123"
    assert msg.target == "target456"
    assert msg.action == "cmd"
    assert msg.args == ["arg1", "arg2"]

def test_invalid_message_missing_at():
    with pytest.raises(InvalidMessageError):
        Message("user123target456/cmd")

def test_invalid_message_missing_slash():
    with pytest.raises(InvalidMessageError):
        Message("user123@target456cmd")

def test_invalid_message_missing_user():
    with pytest.raises(InvalidMessageError):
        Message("@target456/cmd")

def test_invalid_message_missing_target_id():
    with pytest.raises(InvalidMessageError):
        Message("user123@/cmd")

def test_invalid_characters_in_user():
    with pytest.raises(InvalidMessageError):
        Message("user!23@target456/cmd")

def test_invalid_characters_in_target_id():
    with pytest.raises(InvalidMessageError):
        Message("user123@target!456/cmd")

def test_valid_message_with_underscores():
    msg = Message("user_123@target_456/cmd arg1 arg2")
    assert msg.user == "user_123"
    assert msg.target == "target_456"
    assert msg.action == "cmd"
    assert msg.args == ["arg1", "arg2"]
