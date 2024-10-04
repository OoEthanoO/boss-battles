from .character import Stats


class AbilityRegistry:
    registry = {}

    @classmethod
    def register(cls, ability_identifier: str, ability_class):
        """
        Registers a new ability with the given name and class.
        """
        cls.registry[ability_identifier.lower()] = ability_class


class Ability:
    identifier: str
    name: str
    effect: Stats
    cost: Stats

    def __init_subclass__(cls, **kwargs):
        """
        Automatically registers subclasses of Ability in the AbilityRegistry
        based on their defined 'name' attribute.
        """
        super().__init_subclass__(**kwargs)
        if hasattr(cls, 'identifier'):
            AbilityRegistry.register(cls.identifier, cls)

    def verify(self, op_token, solve_token):
        return solve_token == self.algorithm(op_token)

    def algorithm(self, op_token):
        pass


class BasicAttack(Ability):
    identifier = "attack"
    name = "Basic Attack"
    effect = Stats(health=-5)
    cost = Stats(stamina=-5)

    def algorithm(self, op_token):
        return ""

    def verify(self, op_token, solve_token):
        # Basic attack is always castable
        return True
    

class Bite(Ability):
    identifier = "bite"
    name = "Bite"
    effect = Stats(health=-1)
    cost = Stats(stamina=-1)  # dignity -50

    def algorithm(self, op_token):
        return ""

    def verify(self, op_token, solve_token):
        # Bite is always castable
        return True


class Cower(Ability):
    identifier = "cower"
    name = "Cower"
    effect = Stats()
    cost = Stats()

    def algorithm(self, op_token):
        return ""

    def verify(self, op_token, solve_token):
        # Bite is always castable
        return True


class SwiftStrike(Ability):
    identifier = "sstrike"
    name = "Swift Strike"
    effect = Stats(health=-10)
    cost = Stats(stamina=-5)

    def algorithm(self, op_token):
        return op_token


class Heal(Ability):
    identifier = "heal"
    name = "Heal"
    effect = Stats(health=5)
    cost = Stats(mana=-5)

    def algorithm(self, op_token):
        return op_token[::-1]

