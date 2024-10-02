from game import Stats

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
    
attack_obj = BasicAttack()
heal_obj = Heal()
print(attack_obj.verify("ac", "abc"))
print(heal_obj.verify("cba", "abc"))