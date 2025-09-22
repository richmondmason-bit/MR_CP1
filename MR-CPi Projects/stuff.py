import random as rnd  # Importing random as rnd to avoid conflicts
import time  # Import time for the delay function

# Player Stats
player_hp = 20
player_attack = 2
player_damage = 5
player_defense = 3
player_heal_amount = 5

# Monster Stats
monster_hp = 15
monster_attack = 3
monster_damage = 10
monster_defense = 2

# Functions for Actions
def player_turn(player_hp, monster_hp):
    print("\nYour Turn:")
    action = input("Do you want to (A)ttack or (H)eal? ").lower()
    
    # If the player chooses to attack
    if action == 'a':
        hit_roll = rnd.randint(1, 20) + player_attack
        damage_roll = rnd.randint(1, 8) + player_damage

        if hit_roll > 12:
            print("You hit! Roll for damage!")
            damage_dealt = max(damage_roll - monster_defense, 0)
            print(f"You did {damage_dealt} damage!")
            monster_hp -= damage_dealt

            if monster_hp <= 0:
                print("The monster has been defeated!")
                return player_hp, 0  # Player wins
        else:
            print("You missed!")
    
    # If the player chooses to heal
    elif action == 'h':
        print(f"You heal for {player_heal_amount} HP!")
        player_hp = min(player_hp + player_heal_amount, 20)  # Max HP is 20
    
    # If invalid input, re-prompt the player
    else:
        print("Invalid action. Please choose again.")
        return player_turn(player_hp, monster_hp)  # Recursive call to prompt again
    
    return player_hp, monster_hp

def monster_turn(player_hp, monster_hp):
    print("\nMonster's Turn:")
    hit_roll = rnd.randint(1, 20) + monster_attack
    damage_roll = rnd.randint(1, 8) + monster_damage

    if hit_roll > 12:
        print("The monster hits! Roll for damage!")
        damage_dealt = max(damage_roll - player_defense, 0)
        print(f"The monster did {damage_dealt} damage!")
        player_hp -= damage_dealt

        if player_hp <= 0:
            print("You have been defeated by the monster!")
            return 0, monster_hp  # Monster wins
    else:
        print("The monster missed!")

    return player_hp, monster_hp

# Game Loop
def game_loop():
    player_hp = 20
    monster_hp = 15

    print("A wild monster appears!")
    print(f"Monster HP: {monster_hp} | Your HP: {player_hp}")

    while player_hp > 0 and monster_hp > 0:
        # Player's turn
        player_hp, monster_hp = player_turn(player_hp, monster_hp)
        time.sleep(1)  # Adding a small delay for better flow
        if monster_hp <= 0:
            break  # Exit loop if player wins

        # Monster's turn
        player_hp, monster_hp = monster_turn(player_hp, monster_hp)
        time.sleep(1)  # Adding a small delay for better flow
        if player_hp <= 0:
            break  # Exit loop if monster wins

        print(f"Monster HP: {monster_hp} | Your HP: {player_hp}")

    # Final outcome
    if player_hp <= 0:
        print("\nGame Over. You were defeated.")
    elif monster_hp <= 0:
        print("\nCongratulations! You defeated the monster!")

# Start the game
game_loop()

