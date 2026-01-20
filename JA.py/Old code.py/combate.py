import random
import time


classes = {
    1: {"name": "Fighter", "health": 30, "defense": 14, "attack_bonus": 3, "damage_bonus": 4, "damage_die": 8},
    2: {"name": "Mage", "health": 24, "defense": 12, "attack_bonus": 5, "damage_bonus": 2, "damage_die": 10},
    3: {"name": "Rogue", "health": 26, "defense": 13, "attack_bonus": 4, "damage_bonus": 3, "damage_die": 6}
}

def roll(die):
    return random.randint(1, die)


def player_turn(player, monster):
    print("\nYour turn!")
    print("1. Normal Attack")
    print("2. Wild Attack (double damage but hurt yourself)")
    print("3. Drink a healing potion (+9 health)")
    print("4. Flee (50% chance to escape)")

    choice = input("Choose: ")

    if choice == "1":
        attack_roll = roll(20) + player["attack_bonus"]
        if attack_roll >= monster["defense"]:
            damage = roll(player["damage_die"]) + player["damage_bonus"]
            monster["health"] -= damage
            print("You hit the monster for", damage, "damage!")
        else:
            ("what are you doing?")
          

    elif choice == "2":
        attack_roll = roll(20) + player["attack_bonus"]
        if attack_roll >= monster["defense"]:
            damage = (roll(player["damage_die"]) + player["damage_bonus"]) * 2
            monster["health"] -= damage
            print("You went wild and did", damage, "damage!")
            player["health"] -= 3
            print("But you hurt yourself for 3 damage.")
        else:
            print("You missed and hurt yourself a little!")
            player["health"] -= 2

    elif choice == "3":
        player["health"] += 9
        print("You drank a potion and regained 9 health!")

    elif choice == "4":
        if random.random() < 0.5:
            print("You escaped successfully!")
            return "fled"
        else:
            print("You tried to flee but failed!")

    else:
        print("Invalid choice.")

def monster_turn(player, monster):
    print("\nMonster's turn!")
    time.sleep(1)
    attack_roll = roll(20) + monster["attack_bonus"]
    if attack_roll >= player["defense"]:
        damage = roll(monster["damage_die"]) + monster["damage_bonus"]
        player["health"] -= damage
        print("The", monster["name"], "hit you for", damage, "damage!")
    else:
        print("The", monster["name"], "missed!")

print("Welcome to training! First I need to know some things about you!\n")

player_name = input("What is your name? ")

print("\nWhat class of fighter are you?")
print("1 if you are a Fighter")
print("2 if you are a Mage")
print("3 if you are a Rogue")

choice = input("Choose: ")

if choice.isdigit() and int(choice) in classes:
    player = classes[int(choice)].copy()
else:
    print("Invalid choice, defaulting to Fighter.")
    player = classes[1].copy()

player["name"] = player_name

print("\nGreat, here are your stats!")
print("Health:", player["health"])
print("Defense:", player["defense"])
print("Attack: D20 +", player["attack_bonus"])
print("Damage: D" + str(player["damage_die"]), "+", player["damage_bonus"])

# Create a monster
monster = {"name": "Dire Wolf", "health": 35, "defense": 13, "attack_bonus": 2, "damage_bonus": 2, "damage_die": 8}

print("\nYou are being attacked by a Dire Wolf!")
time.sleep(1)

# Randomly decide who goes first
if random.choice([True, False]):
    print("\nYou move first!")
    player_first = True
else:
    print("\nThe Dire Wolf moves first!")
    player_first = False


while player["health"] > 0 and monster["health"] > 0:
    if player_first:
        result = player_turn(player, monster)
        if result == "fled":
            break
        if monster["health"] <= 0:
            print("\nYou defeated the Dire Wolf!")
            break
        monster_turn(player, monster)
    else:
        monster_turn(player, monster)
        if player["health"] <= 0:
            break
        result = player_turn(player, monster)
        if result == "fled":
            break

    print("\nYour Health:", player["health"], "| Dire Wolf Health:", monster["health"])
    print("-" * 40)
    time.sleep(1)


if player["health"] <= 0:
    print("\nYou were defeated... Game over.")
elif monster["health"] <= 0:
    print("\nVictory! You won!")
else:
    print("\nYou ran away safely!")



