import pytest
from boss_battles.ability import AbilityRegistry, BasicAttack, Heal
from boss_battles.character import Stats

def test_basic_attack_algorithm():
    basic_attack = BasicAttack()
    
    # Test the algorithm method of BasicAttack
    result = basic_attack.algorithm("abcde")
    assert result == "ace", "BasicAttack algorithm failed"

def test_basic_attack_verification():
    basic_attack = BasicAttack()
    
    # Test the verify method of BasicAttack
    assert basic_attack.verify("abcd", "ac") == True, "BasicAttack verify failed with correct solve_token"
    assert basic_attack.verify("abc", "ac") == True, "BasicAttack verify failed with correct solve_token"
    assert basic_attack.verify("abcd", "xx") == False, "BasicAttack verify failed with incorrect solve_token"

def test_heal_algorithm():
    heal = Heal()
    
    # Test the algorithm method of Heal
    result = heal.algorithm("abcd")
    assert result == "dcba", "Heal algorithm failed"

def test_heal_verification():
    heal = Heal()
    
    # Test the verify method of Heal
    assert heal.verify("abcd", "dcba") == True, "Heal verify failed with correct solve_token"
    assert heal.verify("abcd", "xx") == False, "Heal verify failed with incorrect solve_token"

def test_registry_contains_abilities():
    # Test that abilities have been correctly registered in the AbilityRegistry
    assert "attack" in AbilityRegistry.registry, "BasicAttack was not registered in the AbilityRegistry"
    assert "heal" in AbilityRegistry.registry, "Heal was not registered in the AbilityRegistry"
    
    # Test that registered classes are correct
    assert AbilityRegistry.registry["attack"] == BasicAttack, "BasicAttack registration failed"
    assert AbilityRegistry.registry["heal"] == Heal, "Heal registration failed"

def test_registry_lookup():
    # Test the registry lookup and instantiation of abilities
    ability_class = AbilityRegistry.registry.get("attack")
    assert ability_class is BasicAttack, "Registry lookup for BasicAttack failed"
    
    # Instantiate and use the ability
    ability_instance = ability_class()
    assert ability_instance.verify("abcd", "ac") == True, "Registry lookup for BasicAttack instantiation failed"
    
    ability_class = AbilityRegistry.registry.get("heal")
    assert ability_class is Heal, "Registry lookup for Heal failed"
    
    # Instantiate and use the ability
    ability_instance = ability_class()
    assert ability_instance.verify("dcba", "abcd") == True, "Registry lookup for Heal instantiation failed"

