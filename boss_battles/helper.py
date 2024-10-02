def parse(data):
    at_index = data.find("@")
    if at_index == -1:
        return None
    
    caster = data[:at_index]

    slash_index = data[at_index + 1:].find("/")
    if slash_index == -1:
        return None
    
    target = data[at_index + 1:at_index + slash_index + 1]

    colon_index = data[at_index + slash_index + 2:].find(":")
    if colon_index == -1:
        return None
    
    attack_name = data[at_index + slash_index + 2:at_index + slash_index + colon_index + 2]

    solve_token = data[at_index + slash_index + colon_index + 3:]

    return {
        "caster": caster,
        "target": target,
        "attack_name": attack_name,
        "solve_token": solve_token
    }