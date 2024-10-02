from .game import BossBattle
from .character import Squirrel, Player
from .utils import print_health_list
from .message import Message, InvalidMessageError

bosses = [
    Squirrel()
]

players = [
    Player("mrgallo")
]

battle = BossBattle(players=players, bosses=bosses)

print("Running game")
print("Boss{}: {}".format('es' if len(battle._bosses) > 1 else '', ', '.join(map(str.upper, [b._name for b in battle._bosses]))))
print()
print("Players:\n" + "\n".join(map(str.upper, [p._name for p in battle._players])))
while battle.next_round():
    print("=" * 10 + " ROUND " + str(battle.get_round()) + " " + "=" * 10)
    print_health_list("BOSSES", battle._bosses)
    print_health_list("PLAYERS", battle._players)
    print()

    opportunity_tokens = battle.get_opportunity_tokens()
    print("OPPORTUNITY TOKEN{}".format("S" if len(opportunity_tokens) > 1 else ""))
    for token in opportunity_tokens:
        print(token)
    print()

    # get actions from players
    valid_messages = []
    for player in players:
        action = player._name.lower() + "@" + input("{}, enter action string: {}@".format(player._name, player._name.lower()))
        try:
            valid_messages.append(Message(action))
        except InvalidMessageError as e:
            print("Invalid message: '{}'".format(action))
    
    battle.handle_actions(valid_messages)

    # boss action

