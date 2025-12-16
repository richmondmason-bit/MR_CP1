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

print("Your grades have hit STRAIGHT D's.")
print("Fight through the school and reach the principal and face him down for mistreatment by teachers, word of this courage to demand time from the principal has made the teachers foam for the mouth..\n")
player_hp = 30
player_max_hp = 30
player_level = 1
player_xp = 0
player_xp_next = 10
player_gold = 0
weapon_name = "Fists"
weapon_damage = 3
inventory = ["Potion"]
potions = 1
rooms = [
    {
        "name": "Hallway",
        "desc": "A long dark corridor.",
        "enemy_name": "Bully Helper",
        "enemy_hp": 25,
        "enemy_max_hp": 25,
        "enemy_attack": 8,
        "enemy_potions": 1,
        "xp": 8,
        "done": False
    },
    {
        "name": "Library",
        "desc": "Shelves of dusty books.",
        "enemy_name": "Anime Nerd",
        "enemy_hp": 35,
        "enemy_max_hp": 35,
        "enemy_attack": 10,
        "enemy_potions": 2,
        "xp": 12,
        "done": False
    },
    {
        "name": "Math Class",
        "desc": "Textbooks and eraser dust floating.",
        "enemy_name": "Math Nerd",
        "enemy_hp": 60,
        "enemy_max_hp": 60,
        "enemy_attack": 12,
        "enemy_potions": 2,
        "xp": 22,
        "done": False
    }
]
while player_hp > 0:
    print("\nRooms:")
    for i in range(len(rooms)):
        status = "Completed" if rooms[i]["done"] else "New"
        print(i + 1, rooms[i]["name"], "-", status)
    choice = input("Choose room number or quit: ")
    if choice == "quit":
        break
    if not choice.isdigit():
        continue
    choice = int(choice) - 1
    if choice < 0 or choice >= len(rooms):
        continue
    room = rooms[choice]
    if room["done"]:
        print("You've already cleared this room.")
        continue
    print("\n===", room["name"], "===")
    print(room["desc"])
    enemy_hp = room["enemy_hp"]
    enemy_max_hp = room["enemy_max_hp"]
    enemy_attack = room["enemy_attack"]
    enemy_potions = room["enemy_potions"]
    print("A", room["enemy_name"], "appears!")
    while enemy_hp > 0 and player_hp > 0:
        print("\nYour HP:", player_hp, "/", player_max_hp)
        print(room["enemy_name"], "HP:", enemy_hp, "/", enemy_max_hp)
        print("attack / potion")
        action = input("> ")
        if action == "attack":
            dmg = random.randint(1, 6) + weapon_damage
            enemy_hp -= dmg
            print("You deal", dmg)
        elif action == "potion":
            if potions > 0:
                heal = random.randint(8, 15)
                player_hp += heal
                if player_hp > player_max_hp:
                    player_hp = player_max_hp
                potions -= 1
                print("You heal", heal)
            else:
                print("No potions!")
        if enemy_hp <= 0:
            break
        enemy_dmg = random.randint(1, enemy_attack)
        player_hp -= enemy_dmg
        print(room["enemy_name"], "hits you for", enemy_dmg)
        if enemy_hp < enemy_max_hp // 3 and enemy_potions > 0:
            heal = random.randint(6, 12)
            enemy_hp += heal
            enemy_potions -= 1
            print(room["enemy_name"], "uses a potion!")
    if player_hp > 0:
        print("You defeated", room["enemy_name"])
        player_xp += room["xp"]
        gold = random.randint(5, 10)
        player_gold += gold
        print("Gained", room["xp"], "XP and", gold, "gold")
        room["done"] = True
    else:
        print("You died.")
        break
print("\nGame over.")
