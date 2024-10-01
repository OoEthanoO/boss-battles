import pytest
import time


from boss_battles.fake_radio import FakeRadio


def test_radio_empty_cache_returns_none():
    radio1 = FakeRadio()
    assert radio1.receive() is None
    assert radio1.receive_full() is None

# Test for the send method of FakeRadio
def test_fake_radio_send():
    radio1 = FakeRadio(group=1)
    radio2 = FakeRadio(group=1)
    
    # Radio 1 sends a message
    radio1.send("Hello")
    
    # Radio 2 should receive the message
    assert radio2.receive() == "Hello"


# Test for the receive method of FakeRadio
def test_fake_radio_receive():
    radio1 = FakeRadio(group=1)
    radio2 = FakeRadio(group=1)

    # Send a message from radio1 to radio2
    radio1.send("Hello World")

    # Verify radio2 received the message
    assert radio2.receive() == "Hello World"


# Test for receive_full method of FakeRadio
def test_fake_radio_receive_full():
    radio1 = FakeRadio(group=1)
    radio2 = FakeRadio(group=1)

    # Send a message from radio1 to radio2
    radio1.send("Test Message")

    # Receive full details on radio2 (message, rssi, timestamp)
    message, rssi, timestamp = radio2.receive_full()

    # Check if the message is correct
    assert message == "Test Message"
    
    # Check if the RSSI is 0 (as per _add_message_to_queue method)
    assert rssi == 0
    
    # Check if timestamp is recent (within 1 second)
    assert abs(time.time() * 1000 - timestamp) < 1000


# Test sending and receiving between radios in different groups
def test_fake_radio_different_groups():
    radio1 = FakeRadio(group=1)
    radio2 = FakeRadio(group=2)

    # Send a message from radio1 to radio2
    radio1.send("Message to different group")

    # Verify that radio2 did not receive the message
    radio2.receive() is None


# Test cache size (max length of the message queue)
def test_fake_radio_cache_size():
    radio1 = FakeRadio(group=1)
    radio2 = FakeRadio(group=1, cache_size=2)  # Set cache size to 2

    # Send multiple messages
    radio1.send("Message 1")
    radio1.send("Message 2")
    radio1.send("Message 3")

    # Only the last two messages should remain in radio2's queue
    assert radio2.receive() == "Message 2"
    assert radio2.receive() == "Message 3"

    # No more messages should be available in the queue
    radio2.receive() is None

