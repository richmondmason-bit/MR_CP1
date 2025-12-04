

#FUNCTION start_matrix_intro():
    #CLEAR screen
    #START matrix rain for a few seconds
    #STOP matrix rain
    #CALL print_matrix_text("WELCOME TO THE FACILITY")
    #CALL print_matrix_text("INITIALIZING SYSTEM...")

#FUNCTION start_matrix_rain(duration):
    #SET start_time = current time

    #WHILE current time - start_time < duration:
        #FOR each column on screen:
            #DRAW random green characters falling downward
        #UPDATE screen
        #BRIGHT_GREEN = "\033[38;5;46m"
        #SMALL delay
    #END WHILE

#FUNCTION stop_matrix_rain():
    #CLEAR all falling characters
    #RESET cursor to top-left

#FUNCTION print_matrix_text(text):
    #FOR each character in text:

        #CHOOSE a random vertical drop height

        #FOR y from 0 to drop height:
            #DRAW character at (x, y) in dim green
            #ERASE previous position
            #SHORT delay

        #DRAW character at final position in bright green

    #MOVE cursor to next line

#FUNCTION main():
    #CALL start_matrix_intro()

    #WHILE game is running:
        #CALL hallway()

#FUNCTION hallway():
   # CALL print_matrix_text("=== HALLWAY ===")
    #CALL print_matrix_text("HP: " + player.hp)
   # CALL print_matrix_text("Items: " + list_of_player_items)

    #SHOW list of available rooms using print_matrix_text()

    #INPUT player choice

    #IF chosen room exists:
    #    CALL that room's function
    #ELSE:
       # CALL print_matrix_text("Invalid choice.")

#FUNCTION room_name():
    #CALL print_matrix_text("You entered the room.")

    #IF room_not_completed:
        #RUN special event (fight / item / puzzle)
        #SET room_completed = true
        #CALL print_matrix_text("Room completed.")
    #ELSE:
        #CALL print_matrix_text("Nothing new here.")



#FUNCTION pickup_item(item):
    #IF player does NOT have item:
     #   ADD item to inventory
      #  CALL print_matrix_text("Picked up: " + item)
    #ELSE:
     #   CALL print_matrix_text("You already have that item.")


#FUNCTION combat(enemy):
  #  CALL print_matrix_text("Combat started: " + enemy.name)

   # WHILE player HP > 0 AND enemy HP > 0:

    #    ASK player for choice: attack / dodge / item

     #   IF attack:
      #      DEAL damage to enemy
       #     CALL print_matrix_text("You strike " + enemy.name)

        #IF dodge:
         #   IF success:
          #      CALL print_matrix_text("You dodged the attack!")
           #     CONTINUE to next loop without enemy attacking

       # IF item:
        #    IF item usable:
         #       APPLY effect
          #      CALL print_matrix_text("Item used.")
           # ELSE:
            #    CALL print_matrix_text("No usable items.")

   #     IF enemy still alive:
    #        ENEMY attempts attack (may miss)
     #       CALL print_matrix_text(enemy attack result)

    #END WHILE

    #IF player HP <= 0:
     #   CALL print_matrix_text("You died.")
    #ELSE:
     #   CALL print_matrix_text(enemy.name + " defeated!")



#IMPORTANT MESSAGE i used chatgpt to help me with the martix rain effect because i didnt know really how to implement the matrix rain i did with printing text

import random
import sys
import time

GREEN = "\033[38;2;0;255;70m"
RESET = "\033[0m"

def matrix_print(text, speed=0.01):
    for char in text:
        sys.stdout.write(GREEN + char + RESET)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def roll(dice):
    return random.randint(1, dice)

class Player:
    def __init__(self):
        self.name = "Hero"
        self.level = 1
        self.xp = 0
        self.xp_to_next = 10
        self.max_hp = 30
        self.hp = self.max_hp
        self.gold = 0
        self.inventory = ["Potion"]
        self.weapons = {
            "Fists": 3,
            "Spork": 6,
            "Eraser Blade": 10
        }
        self.selected_weapon = "Fists"
        self.special_cooldown = 0
        self.shield_ready = True
        self.dodge_ready = True

    def add_xp(self, amount):
        self.xp += amount
        matrix_print(f"Gained {amount} XP.")
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp_to_next = int(self.xp_to_next * 1.5)
        self.max_hp += 5
        self.hp = self.max_hp
        # small attack bump per level
        # increase all base attack-ish behavior by 1
        matrix_print(f"LEVEL UP! You are now level {self.level}.")
        matrix_print(f"Max HP increased to {self.max_hp}. Attack power increased.")
        # increase a generic stat: we'll add +1 to all weapon base as a simple proxy to attack increase
        for k in self.weapons:
            self.weapons[k] += 0  # keep weapon base, player's "attack" is reflected via selected weapon damage scale
        # also grant small permanent attack via adding to a simple attribute
        # we reflect this by an implied player bonus in combat: using level in damage calculation

class Room:
    def __init__(self, name, description, enemy=None, item=None):
        self.name = name
        self.description = description
        self.enemy = enemy
        self.item = item
        self.completed = False

    def enter(self, player):
        matrix_print(f"=== {self.name} ===")
        matrix_print(self.description)
        if self.item and self.item not in player.inventory:
            player.inventory.append(self.item)
            matrix_print(f"Picked up: {self.item}")
        if self.enemy and not self.completed:
            # copy enemy so base data isn't permanently mutated across attempts
            enemy = {
                "name": self.enemy["name"],
                "hp": self.enemy["hp"],
                "max_hp": self.enemy["max_hp"],
                "attack": self.enemy["attack"],
                "special_cd": self.enemy.get("special_cd", 0),
                "potions": self.enemy.get("potions", 0),
                "xp_reward": self.enemy.get("xp_reward", 0)
            }
            combat(player, enemy)
        self.completed = True

def enemy_turn(player, enemy):
    if enemy["hp"] <= 0:
        return

    # enemy special attack — uses cooldown
    if enemy["special_cd"] == 0 and roll(4) == 1:
        dmg = roll(enemy["attack"]) + 5
        matrix_print(f"{enemy['name']} uses SPECIAL ATTACK for {dmg}!")
        player.hp -= dmg
        enemy["special_cd"] = 3
        return
    else:
        enemy["special_cd"] = max(0, enemy["special_cd"] - 1)

    # enemy potion use
    if enemy["hp"] <= enemy["max_hp"] // 3 and enemy["potions"] > 0:
        heal = random.randint(6, 12)
        enemy["hp"] += heal
        enemy["potions"] -= 1
        matrix_print(f"{enemy['name']} drinks a potion and heals {heal}!")
        return

    # normal attack
    dmg = roll(enemy["attack"])
    matrix_print(f"{enemy['name']} hits you for {dmg}!")
    player.hp -= dmg

def combat(player, enemy):
    matrix_print(f"A {enemy['name']} appears!")
    dodge_momentum = 0

    while enemy["hp"] > 0 and player.hp > 0:
        matrix_print(f"Your HP: {player.hp}/{player.max_hp} | Enemy HP: {enemy['hp']}/{enemy['max_hp']}")
        matrix_print(f"Level: {player.level} | XP: {player.xp}/{player.xp_to_next} | Gold: {player.gold}")
        matrix_print(f"Weapon: {player.selected_weapon} (DMG: {player.weapons[player.selected_weapon]})")
        matrix_print("Actions: attack, special, dodge, shield, potion, weapon, run")

        action = input("> ").lower().strip()

        shield_active = False

        # attack
        if action == "attack":
            base_weapon = player.weapons.get(player.selected_weapon, 1)
            dmg = roll(6) + base_weapon + (player.level - 1)  # level contributes to damage
            enemy["hp"] -= dmg
            matrix_print(f"You hit with {player.selected_weapon} for {dmg}!")

        # special attack with cooldown
        elif action == "special":
            if player.special_cooldown > 0:
                matrix_print(f"Special attack cooling down ({player.special_cooldown} turns left)")
                # enemy gets a turn if you wasted action
                enemy_turn(player, enemy)
                player.special_cooldown = max(0, player.special_cooldown - 1)
                continue
            sp = roll(10) + player.weapons.get(player.selected_weapon, 1) * 2 + (player.level - 1)
            enemy["hp"] -= sp
            matrix_print(f"You unleash a SPECIAL ATTACK for {sp}!")
            player.special_cooldown = 3

        # dodge (one-time per enemy turn with ready flag)
        elif action == "dodge":
            if not player.dodge_ready:
                matrix_print("You cannot dodge again yet!")
                enemy_turn(player, enemy)
                # cooldowns tick below
                player.dodge_ready = True
                continue
            matrix_print("You attempt to dodge...")
            if roll(2) == 1:
                matrix_print("You dodge successfully and take no damage this turn!")
                dodge_momentum = 1
            else:
                matrix_print("Failed to dodge!")
                dodge_momentum = 0
                enemy_turn(player, enemy)
            player.dodge_ready = False
            # cooldowns tick below
            continue

        # shield reduces enemy damage for their turn
        elif action == "shield":
            if not player.shield_ready:
                matrix_print("Shield not ready!")
                enemy_turn(player, enemy)
                player.shield_ready = True
                continue
            reduce = roll(4) + 3
            matrix_print(f"You brace with your shield, will reduce up to {reduce} damage this enemy attack.")
            # apply enemy turn but reduce damage
            old_hp = player.hp
            enemy_turn(player, enemy)
            damage_taken = old_hp - player.hp
            mitigated = min(reduce, damage_taken)
            player.hp += mitigated
            matrix_print(f"Shield mitigated {mitigated} damage.")
            player.shield_ready = False
            # cooldowns tick below
            player.special_cooldown = max(0, player.special_cooldown - 1)
            continue

        # potion heal
        elif action == "potion":
            if "Potion" not in player.inventory:
                matrix_print("No potions left!")
            else:
                heal = random.randint(8, 15)
                player.hp = min(player.max_hp, player.hp + heal)
                player.inventory.remove("Potion")
                matrix_print(f"You drink a potion and heal {heal} HP!")

        # weapon selection menu
        elif action == "weapon":
            matrix_print("Available weapons:")
            for w, dmg_val in player.weapons.items():
                matrix_print(f"{w} (DMG {dmg_val})")
            pick = input("Choose weapon> ").strip()
            # allow direct title-casing fallback, but prefer exact match
            if pick in player.weapons:
                player.selected_weapon = pick
                matrix_print(f"Switched to {pick}")
            else:
                # try title-case
                t = pick.title()
                if t in player.weapons:
                    player.selected_weapon = t
                    matrix_print(f"Switched to {t}")
                else:
                    matrix_print("Invalid weapon choice.")

        # run attempt
        elif action == "run":
            if roll(2) == 1:
                matrix_print("You escaped!")
                return
            else:
                matrix_print("Failed to escape!")
                enemy_turn(player, enemy)

        else:
            matrix_print("Invalid action.")

        # check enemy death after player's successful actions
        if enemy["hp"] <= 0:
            matrix_print(f"You defeated the {enemy['name']}!")
            gold = roll(8) + enemy.get("max_hp", 0) // 5
            xp = enemy.get("xp_reward", roll(6) + enemy.get("max_hp", 0) // 5)
            player.gold += gold
            matrix_print(f"You gain {gold} gold.")
            player.add_xp(xp)
            return

        # enemy turn, considering dodge momentum
        if dodge_momentum > 0:
            matrix_print("Your dodge momentum avoids the enemy attack this turn.")
            dodge_momentum = max(0, dodge_momentum - 1)
        else:
            enemy_turn(player, enemy)

        # tick cooldowns and reset per-turn ready flags
        player.special_cooldown = max(0, player.special_cooldown - 1)
        # shield and dodge regain each full turn loop so they can't be spammed — require next turn to use again
        player.shield_ready = True
        player.dodge_ready = True

        if player.hp <= 0:
            matrix_print("You died...")
            return

def shop(player):
    matrix_print("=== SHOP ===")
    # Basic shop with fixed prices, no refresh
    stock = {
        "Potion": 10,
        "Spork": 25,
        "Eraser Blade": 60
    }
    matrix_print("Welcome. Items for sale:")
    for item, price in stock.items():
        matrix_print(f"{item} - {price} gold")
    matrix_print(f"Your Gold: {player.gold}")
    matrix_print("Type item name to buy, or 'leave' to exit.")
    while True:
        choice = input("> ").strip()
        if choice.lower() == "leave":
            matrix_print("Leaving shop.")
            return
        if choice in stock:
            price = stock[choice]
            if player.gold < price:
                matrix_print("You can't afford that.")
                continue
            player.gold -= price
            # apply purchase effects
            if choice == "Potion":
                player.inventory.append("Potion")
                matrix_print("Purchased Potion.")
            else:
                if choice not in player.weapons:
            
                    if choice == "Spork":
                        player.weapons["Spork"] = 6
                    elif choice == "Eraser Blade":
                        player.weapons["Eraser Blade"] = 10
                matrix_print(f"Purchased {choice}. Added to your weapons.")
            matrix_print(f"Gold remaining: {player.gold}")
        else:
            matrix_print("Item not found in shop.")
def main():
    player = Player()
    rooms = [
        Room("Hallway", "A long dark corridor.",
             enemy={"name": "Bully Helper", "hp": 25, "max_hp": 25, "attack": 8, "special_cd": 0, "potions": 1, "xp_reward": 8},
             item="Spork"),
        Room("Library", "Shelves of dusty books.",
             enemy={"name": "Anime nerd", "hp": 35, "max_hp": 35, "attack": 10, "special_cd": 0, "potions": 2, "xp_reward": 12},
             item="Potion"),

        Room("Math Class", "Textbooks and eraser dust floating.",
             enemy={"name": "Math Nerd", "hp": 60, "max_hp": 60, "attack": 12, "special_cd": 0, "potions": 2, "xp_reward": 22},
             item="Eraser Blade")
    ]

    while player.hp > 0:
        matrix_print("Rooms:")
        for i, room in enumerate(rooms):
            matrix_print(f"{i+1}. {room.name} ({'Completed' if room.completed else 'New'})")
        matrix_print("'shop' to enter the shop | 'status' to view status | 'quit' to exit")
        choice = input("> ").strip().lower()
        if choice == "quit":
            matrix_print("Exiting...")
            return
        if choice == "shop":
            shop(player)
            continue
        if choice == "status":
            matrix_print(f"Level: {player.level} | XP: {player.xp}/{player.xp_to_next} | HP: {player.hp}/{player.max_hp} | Gold: {player.gold}")
            matrix_print(f"Weapons: {list(player.weapons.keys())} | Inventory: {player.inventory}")
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(rooms):
            rooms[int(choice) - 1].enter(player)
        else:
            matrix_print("Invalid choice.")
        matrix_print(f"HP: {player.hp} | Gold: {player.gold} | Inventory: {player.inventory}")
if __name__ == "__main__":
    main()
