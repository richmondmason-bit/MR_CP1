import random
print("Your grades have hit STRAIGHT D's.")
print("You must fight through the school and reach the principal.\n")
player_name = "Clint Eastwood"
player_level = 1
player_xp = 0
player_xp_next = 10
player_max_hp = 30
player_hp = 30
player_gold = 0
inventory = ["Potion"]
weapons = {
    "Fists": 3,
    "Spork": 6,
    "Eraser Blade": 7,
    "Hard textbook": 11
}
current_weapon = "Fists"

special_cd = 0
shield_ready = True
dodge_ready = True
rooms = [
    {
        "name": "Hallway",
        "desc": "A long dark corridor.",
        "enemy": {
            "name": "Bully Helper",
            "hp": 25,
            "max_hp": 25,
            "attack": 8,
            "potions": 1,
            "special_cd": 0,
            "xp": 8
        },
        "item": "Spork",
        "done": False
    },
    {
        "name": "Library",
        "desc": "Shelves of dusty books.",
        "enemy": {
            "name": "Anime Nerd",
            "hp": 35,
            "max_hp": 35,
            "attack": 10,
            "potions": 2,
            "special_cd": 0,
            "xp": 12
        },
        "item": "Potion",
        "done": False
    },
    {
        "name": "Math Class",
        "desc": "Textbooks and eraser dust floating.",
        "enemy": {
            "name": "Math Nerd",
            "hp": 60,
            "max_hp": 60,
            "attack": 12,
            "potions": 2,
            "special_cd": 0,
            "xp": 22
        },
        "item": "Eraser Blade",
        "done": False
    },
    {
        "name": "THE PRINCIPAL'S OFFICE",
        "desc": "His presence crushes your confidence.",
        "enemy": {
            "name": "THE PRINCIPAL",
            "hp": 300,
            "max_hp": 300,
            "attack": 40,
            "potions": 5,
            "special_cd": 0,
            "xp": 666
        },
        "item": None,
        "done": False
    }
]
while player_hp > 0:
    print("\nRooms:")
    for i in range(len(rooms)):
        status = "Completed" if rooms[i]["done"] else "New"
        print(i + 1, rooms[i]["name"], "-", status)
    print("Commands: number / shop / status / quit")
    choice = input("> ").lower()
    if choice == "quit":
        break
    if choice == "status":
        print("\nLevel:", player_level)
        print("XP:", player_xp, "/", player_xp_next)
        print("HP:", player_hp, "/", player_max_hp)
        print("Gold:", player_gold)
        print("Weapon:", current_weapon)
        print("Inventory:", inventory)
        continue
    if choice == "shop":
        print("\nSHOP")
        print("Potion - 10 gold")
        if player_gold >= 10:
            buy = input("Buy potion? yes/no > ")
            if buy == "yes":
                player_gold -= 10
                inventory.append("Potion")
                print("Bought a potion.")
        else:
            print("Not enough gold.")
        continue
    if not choice.isdigit():
        continue
    room_index = int(choice) - 1
    if room_index < 0 or room_index >= len(rooms):
        continue
    room = rooms[room_index]
    if room["done"]:
        print("Already completed.")
        continue
    print("\n===", room["name"], "===")
    print(room["desc"])
    if room["item"] is not None and room["item"] not in inventory:
        inventory.append(room["item"])
        if room["item"] in weapons:
            print("Picked up weapon:", room["item"])
        else:
            print("Picked up:", room["item"])
    enemy = room["enemy"]
    enemy_hp = enemy["hp"]
    enemy_special_cd = enemy["special_cd"]

    print("A", enemy["name"], "appears!")
    while enemy_hp > 0 and player_hp > 0:
        print("\nYour HP:", player_hp, "/", player_max_hp)
        print(enemy["name"], "HP:", enemy_hp, "/", enemy["max_hp"])
        print("Weapon:", current_weapon)
        print("Actions: attack / special / dodge / shield / potion / weapon / run")
        action = input("> ")
        if action == "attack":
            dmg = random.randint(1, 6) + weapons[current_weapon] + (player_level - 1)
            enemy_hp -= dmg
            print("You hit for", dmg)
        elif action == "special":
            if special_cd > 0:
                print("Special on cooldown.")
            else:
                dmg = random.randint(5, 10) + weapons[current_weapon] * 2
                enemy_hp -= dmg
                special_cd = 3
                print("SPECIAL HIT for", dmg)
        elif action == "dodge":
            if dodge_ready:
                if random.randint(1, 2) == 1:
                    print("You dodged!")
                    dodge_ready = False
                    special_cd = max(0, special_cd - 1)
                    continue
                else:
                    print("Dodge failed.")
                dodge_ready = False
            else:
                print("Dodge not ready.")
        elif action == "shield":
            if shield_ready:
                reduce = random.randint(4, 7)
                print("Shield reduces", reduce, "damage.")
                enemy_dmg = random.randint(1, enemy["attack"])
                enemy_dmg = max(0, enemy_dmg - reduce)
                player_hp -= enemy_dmg
                print("You take", enemy_dmg)
                shield_ready = False
                continue
            else:
                print("Shield not ready.")
        elif action == "potion":
            if "Potion" in inventory:
                heal = random.randint(8, 15)
                player_hp += heal
                if player_hp > player_max_hp:
                    player_hp = player_max_hp
                inventory.remove("Potion")
                print("Healed", heal)
            else:
                print("No potions.")
        elif action == "weapon":
            print("Weapons:")
            for w in weapons:
                print("-", w)
            pick = input("> ")
            if pick in weapons:
                current_weapon = pick
                print("Switched to", pick)
        elif action == "run":
            if random.randint(1, 2) == 1:
                print("You escaped!")
                break
            else:
                print("Failed to escape.")
        if enemy_hp <= 0:
            break
        if enemy_special_cd == 0 and random.randint(1, 4) == 1:
            dmg = random.randint(1, enemy["attack"]) + 5
            print(enemy["name"], "uses SPECIAL for", dmg)
            player_hp -= dmg
            enemy_special_cd = 3
        else:
            dmg = random.randint(1, enemy["attack"])
            print(enemy["name"], "hits for", dmg)
            player_hp -= dmg
            enemy_special_cd = max(0, enemy_special_cd - 1)
        if enemy_hp < enemy["max_hp"] // 3 and enemy["potions"] > 0:
            heal = random.randint(6, 12)
            enemy_hp += heal
            enemy["potions"] -= 1
            print(enemy["name"], "heals", heal)
        special_cd = max(0, special_cd - 1)
        dodge_ready = True
        shield_ready = True
    if enemy_hp <= 0:
        print("You defeated", enemy["name"])
        player_xp += enemy["xp"]
        gold = random.randint(5, 10)
        player_gold += gold
        print("Gained", enemy["xp"], "XP and", gold, "gold")
        while player_xp >= player_xp_next:
            player_xp -= player_xp_next
            player_level += 1
            player_xp_next = int(player_xp_next * 1.5)
            player_max_hp += 5
            player_hp = player_max_hp
            print("LEVEL UP! Level", player_level)
        room["done"] = True
    if player_hp <= 0:
        print("You died.")
        break
print("\nGame over.")
