from .character import Stats

# TODO: Should these classes be all static fields and static methods?
#       The values within each of these would-be objects would never change
#       Also, there is no need to create more that one (or any) object of each type.

class Ability:
    def __init__(self, name, action_change, resource_cost):
        self.name = name
        self.action_change = action_change
        self.resource_cost = resource_cost

    def verify(self, solve_token, op_token):
        return solve_token == self.algorithm(op_token)

    def algorithm(self, op_token):
        pass

class BasicAttack(Ability):
    def __init__(self):
        super().__init__("Basic Attack", Stats(health=-5), Stats(stamina=-5))

    def algorithm(self, op_token):
        correct_solve_token = ""
        for i in range(0, len(op_token), 2):
            correct_solve_token += op_token[i]

        return correct_solve_token
    
class Heal(Ability):
    def __init__(self):
        super().__init__("Heal", Stats(health=5), Stats(mana=-5))

    def algorithm(self, op_token):
        return op_token[::-1]


ABILITIES = [BasicAttack, Heal]
