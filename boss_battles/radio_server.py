from microbit import *
import radio


radio.on()
radio.config(group=255)

while True:
    message = radio.receive()
    if message:
        uart.write(message + '\n')
