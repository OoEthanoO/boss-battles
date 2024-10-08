from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .character import Character


def print_health_list(name: str, characters: list['Character']) -> None:
    print(name.upper())
    for c in characters:
        print_health_bar(c, indent_level=1)


def print_health_bar(character: 'Character', indent_level: int=0) -> None:
    output = " " * (indent_level * 4)
    output += (character._name.upper()[:10] + ":").ljust(15)

    total_blocks = 100
    health_blocks = int(character._stats.health / character._base_stats.health * 100)
    health_lost_blocks = total_blocks - health_blocks

    output += f"[{'▓' * health_blocks}{' ' * health_lost_blocks}]"
    output += f" {character._stats.health} / {character._base_stats.health}"
    print(output)
