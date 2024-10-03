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
        correct_solve_token = ""
        for i in range(0, len(op_token), 2):
            correct_solve_token += op_token[i]

        return correct_solve_token


class Heal(Ability):
    identifier = "heal"
    name = "Heal"
    effect = Stats(health=5)
    cost = Stats(mana=-5)

    def algorithm(self, op_token):
        return op_token[::-1]

