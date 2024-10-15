import argparse


from .game_server import GameServer, SerialReader
from .character import Squirrel

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Read from a serial port.")
    
    # Optional arguments with default values
    parser.add_argument(
        '--port', 
        type=str, 
        default='/dev/ttyACM0', 
        help='The serial port to connect to.'
    )
    parser.add_argument(
        '--baud-rate', 
        type=int, 
        default=115200, 
        help='The baud rate for the serial connection.'
    )

    # Parse arguments
    args = parser.parse_args()

    reader = SerialReader(port=args.port, baud_rate=args.baud_rate)
    game = GameServer(bosses=[Squirrel()], reader=reader)
    game.run()

if __name__ == "__main__":
    main()
