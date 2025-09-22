import random

player_hp = 20
player_attack = 2
player_damage = 5
player_defense =3

monster_hp =15
monster_attack =3
monster_damage = 10
monster_defense = 2

hit_roll = random.randint(1,20) + player_attack
damage_roll = random.randint(1,8) + player_attack

if hit_roll > 12:
    print("You Hit! Roll for damage!")
    damage_roll = random.randint(1,8) + player_damage
    if damage_roll > monster_defense:
        print(f"You did {damage_roll-monster_defense}")
    monster_hp -= (damage_roll-monster_defense)
else:
    print("You did no damage.")