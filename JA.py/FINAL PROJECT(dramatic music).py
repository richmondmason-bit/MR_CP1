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
def Matrix_Print(text, speed=0.01):
    for char in text:
        sys.stdout.write(GREEN + char + RESET)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write("\n")
    sys.stdout.flush()
def roll(dice):
    return random.randint(1, dice)
Matrix_Print("Your grades have hit STRAIGHT d's and you must fight through the school and get to the principal to dicuss why you dont deserve these grades...")
class Player:
    def __init__(self):
        self.name = "Clint Eastwood"#put whatever you want here for your name 
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
            "Eraser Blade": 7, #67 LOL OMG 67676767676767676767676767 IM LOSING MY MIND
            "Hard textbook": 11,
            "table saw":40,
            "ARMORED PERSONAL CARRIER": 1100000000000#this is a speedrunner item that sends them to the forever box
        }
        self.selected_weapon = "Fists"
        self.special_cooldown = 0
        self.shield_ready = True
        self.dodge_ready = True
    def add_xp(self, amount):
        self.xp += amount
        Matrix_Print(f"Gained {amount} XP.")
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level_up()
    def level_up(self):
        self.level += 1
        self.xp_to_next = int(self.xp_to_next * 1.5)
        self.max_hp += 5
        self.hp = self.max_hp
        Matrix_Print(f" You are now level {self.level}.")
        Matrix_Print(f" HP increased to {self.max_hp}.")
        for k in self.weapons:
            self.weapons[k] += 0  
class Room:
    def __init__(self, name, description, enemy=None, item=None):
        self.name = name
        self.description = description
        self.enemy = enemy
        self.item = item
        self.completed = False
    def enter(self, player):
        Matrix_Print(f"=== {self.name} ===")
        Matrix_Print(self.description)
        if self.item and self.item not in player.inventory:
            player.inventory.append(self.item)
            Matrix_Print(f"Picked up: {self.item}")
        if self.enemy and not self.completed:
            enemy = {"name": self.enemy["name"],
                "hp": self.enemy["hp"],
                "max_hp": self.enemy["max_hp"],
                "attack": self.enemy["attack"],
                "special_cd": self.enemy.get("special_cd", 0),
                "potions": self.enemy.get("potions", 0),
                "xp_reward": self.enemy.get("xp_reward", 0)}
            combat(player, enemy)
        self.completed = True
def enemy_turn(player, enemy):
    if enemy["hp"] <= 0:
        return
    if enemy["special_cd"] == 0 and roll(4) == 1:
        dmg = roll(enemy["attack"]) + 5
        Matrix_Print(f"{enemy['name']} uses SPECIAL ATTACK for {dmg}!")
        player.hp -= dmg
        enemy["special_cd"] = 3
        return
    else:
        enemy["special_cd"] = max(0, enemy["special_cd"] - 1)
    if enemy["hp"] <= enemy["max_hp"] // 3 and enemy["potions"] > 0:
        heal = random.randint(6, 12)
        enemy["hp"] += heal
        enemy["potions"] -= 1
        Matrix_Print(f"{enemy['name']} drinks a potion and heals {heal}!")
        return
    dmg = roll(enemy["attack"])
    Matrix_Print(f"{enemy['name']} hits you for {dmg}!")
    player.hp -= dmg
def combat(player, enemy):
    Matrix_Print(f"A {enemy['name']} appears!")
    dodge = 0
    while enemy["hp"] > 0 and player.hp > 0:
        Matrix_Print(f"Your HP: {player.hp}/{player.max_hp} | Enemy HP: {enemy['hp']}/{enemy['max_hp']}")
        Matrix_Print(f"Level: {player.level} | XP: {player.xp}/{player.xp_to_next} | Gold: {player.gold}")
        Matrix_Print(f"Weapon: {player.selected_weapon} (DMG: {player.weapons[player.selected_weapon]})")
        Matrix_Print("Actions: attack, special, dodge, shield, potion, weapon, run")
        action = input("> ").lower().strip()
        if action == "attack":
            base_weapon = player.weapons.get(player.selected_weapon, 1)
            dmg = roll(6) + base_weapon + (player.level - 1)  
            enemy["hp"] -= dmg
            Matrix_Print(f"You hit with {player.selected_weapon} for {dmg}!")
        elif action == "special":
            if player.special_cooldown > 0:
                Matrix_Print(f"Special attack cooling down ({player.special_cooldown} turns left)")
                enemy_turn(player, enemy)
                player.special_cooldown = max(0, player.special_cooldown - 1)
                continue
            sp = roll(10) + player.weapons.get(player.selected_weapon, 1) * 2 + (player.level - 1)
            enemy["hp"] -= sp
            Matrix_Print(f"You unleash a SPECIAL ATTACK for {sp}!")
            player.special_cooldown = 3
        elif action == "dodge":
            if not player.dodge_ready:
                Matrix_Print("You cannot dodge again yet!")
                enemy_turn(player, enemy)
                player.dodge_ready = True
                continue
            Matrix_Print("You attempt to dodge...")
            if roll(2) == 1:
                Matrix_Print("You dodge successfully and take no damage this turn!")
                dodge = 1
            else:
                Matrix_Print("Failed to dodge!")
                dodge = 0
                enemy_turn(player, enemy)
            player.dodge_ready = False
            continue
        elif action == "shield":
            if not player.shield_ready:
                Matrix_Print("Shield not ready!")# i am blocking it
                enemy_turn(player, enemy)
                player.shield_ready = True
                continue
            reduce = roll(4) + 3
            Matrix_Print(f"You brace with your shield, will reduce up to {reduce} damage this enemy attack.")
            old_hp = player.hp
            enemy_turn(player, enemy)
            damage_taken = old_hp - player.hp
            damage_dodged = min(reduce, damage_taken)
            player.hp += damage_dodged
            Matrix_Print(f"Shield mitigated {damage_dodged} damage.")
            player.shield_ready = False
            player.special_cooldown = max(0, player.special_cooldown - 1)
            continue
        elif action == "potion":
            if "Potion" not in player.inventory:
                Matrix_Print("No potions left!")
            else:
                heal = random.randint(8, 15)
                player.hp = min(player.max_hp, player.hp + heal)
                player.inventory.remove("Potion")
                Matrix_Print(f"You drink a potion and heal {heal} HP!")
        elif action == "weapon":
            Matrix_Print("Available weapons:")
            for w, dmg_val in player.weapons.items():
                Matrix_Print(f"{w} (DMG {dmg_val})")
            pick = input("Choose weapon> ").strip()
            if pick in player.weapons:
                player.selected_weapon = pick
                Matrix_Print(f"Switched to {pick}")
            else:
                t = pick.title()
                if t in player.weapons:
                    player.selected_weapon = t
                    Matrix_Print(f"Switched to {t}")
                else:
                    Matrix_Print("Invalid weapon choice.")
        elif action == "run":
            if roll(2) == 1:
                Matrix_Print("You escaped!")
                return
            else:
                Matrix_Print("Failed to escape!")
                enemy_turn(player, enemy)
        else:
            Matrix_Print("Invalid action.")
        if enemy["hp"] <= 0:
            Matrix_Print(f"You defeated the {enemy['name']}!")
            gold = roll(8) + enemy.get("max_hp", 0) // 5
            xp = enemy.get("xp_reward", roll(6) + enemy.get("max_hp", 0) // 5)
            player.gold += gold
            Matrix_Print(f"You gain {gold} gold.")
            player.add_xp(xp)
            return
        if dodge > 0:
            Matrix_Print("Your dodge momentum avoids the enemy attack this turn.")
            dodge = max(0, dodge - 1)
        else:
            enemy_turn(player, enemy)
        player.special_cooldown = max(0, player.special_cooldown - 1)
        player.dodge_ready = True

        if player.hp <= 0:
            Matrix_Print("You died...LOL")
            return
def shop(player):
    Matrix_Print("SHOP")
    stock = {"Potion": 10,
        "Spork": 25,
        "Eraser Blade": 60}
    Matrix_Print("Welcome. Items for sale:")
    for item, price in stock.items():
        Matrix_Print(f"{item} - {price} gold")
    Matrix_Print(f"Your Gold: {player.gold}")
    Matrix_Print("Type item name to buy, or 'leave' to exit.")
    while True:
        choice = input("> ").strip()
        if choice.lower() == "leave":
            Matrix_Print("Leaving shop.")
            return
        if choice in stock:
            price = stock[choice]
            if player.gold < price:
                Matrix_Print("You can't afford that.")
                continue
            player.gold -= price
            if choice == "Potion":
                player.inventory.append("Potion")
                Matrix_Print("Purchased Potion.")
            else:
                if choice not in player.weapons:
                    if choice == "Spork":
                        player.weapons["Spork"] = 6
                    elif choice == "Eraser Blade":
                        player.weapons["Eraser Blade"] = 10
                Matrix_Print(f"Purchased {choice}. Added to your weapons.")
            Matrix_Print(f"Gold remaining: {player.gold}")
        else:
            Matrix_Print("Item not found in shop.")
def main():
    player = Player()
    rooms = [
        Room("Hallway", "A long dark corridor.",enemy={"name": "Bully Helper", "hp": 25, "max_hp": 25, "attack": 8, "special_cd": 0, "potions": 1, "xp_reward": 8},item="Spork"),
        Room("Library", "Shelves of dusty books.",enemy={"name": "Anime nerd", "hp": 35, "max_hp": 35, "attack": 10, "special_cd": 0, "potions": 2, "xp_reward": 12},item="Potion"),
        Room("Math Class", "Textbooks and eraser dust floating.",enemy={"name": "Math Nerd", "hp": 60, "max_hp": 60, "attack": 12, "special_cd": 0, "potions": 2, "xp_reward": 22},item="Eraser Blade"),
        Room("History","The most historic thing about this class is the teacher",enemy={"name":"Mr.Macinanti","hp":100,"max_hp": 100,"attack":17,"special_cd":0,"potions:":4,"xp_reward":50}),
        Room("English","The teacher's over-complicated speech with words no-one uses make your brain shrivel in despair ",enemy={"name":"Ms.Thornock","hp":125,"max_hp": 130,"attack":23,"special_cd":0,"potions:":10,"xp_reward":110}),
        Room("Science","Her understanding of the way things work makes her an impeccable foe  ",enemy={"name":"Ms.Krueger","hp":170,"max_hp": 200,"attack":23,"special_cd":0,"potions:":15,"xp_reward":150}),
        Room("Physics ","We have no idea what the teachers name is ..",enemy={"name":"Unknown","hp":220,"max_hp": 220,"attack":27,"special_cd":0,"potions:":15,"xp_reward":210}),
        Room("Hallway group up area ","Students upon students crowd the hallways",enemy={"name":"Valley girl with too much make-up","hp":260,"max_hp": 260,"attack":33,"special_cd":0,"potions:":15,"xp_reward":400}),
        Room("THE PRINCIPAL's OFFICE","His presence makes any student's self esteem crumble",enemy={"name":"THE PRINCIPAL","hp":300,"max_hp": 300,"attack":40,"special_cd":0,"potions:":15,"xp_reward":666}),
        
        
        ]
    while player.hp > 0:
        Matrix_Print("Rooms:")
        for i, room in enumerate(rooms):
            Matrix_Print(f"{i+1}. {room.name} ({'Completed' if room.completed else 'New'})")
        Matrix_Print("'shop' to enter the shop | 'status' to view status | 'quit' to exit")
        choice = input("> ").strip().lower()
        if choice == "quit":
            Matrix_Print("Exiting...bye bye see you later")
            return
        if choice == "shop":
            shop(player)
            continue
        if choice == "status":
            Matrix_Print(f"Level: {player.level} | XP: {player.xp}/{player.xp_to_next} | HP: {player.hp}/{player.max_hp} | Gold: {player.gold}")
            Matrix_Print(f"Weapons: {list(player.weapons.keys())} | Inventory: {player.inventory}")
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(rooms):
            rooms[int(choice) - 1].enter(player)
        else:
            Matrix_Print("Invalid choice.")
        Matrix_Print(f"HP: {player.hp} | Gold: {player.gold} | Inventory: {player.inventory}")
if __name__ == "__main__":
    main()
