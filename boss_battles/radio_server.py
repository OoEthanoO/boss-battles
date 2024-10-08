# This code is run on the radio-server microbit
# which receives actions from players
# and forwards the messages to the game server computer it is attached to.

from microbit import *
import radio


radio.on()
radio.config(group=255)

while True:
    message = radio.receive()
    if message:
        uart.write(message + '\n')
