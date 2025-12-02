

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
import shutil
import sys
import time
import threading

GREEN="\033[38;5;46m"
DIM_GREEN="\033[38;5;28m"
BRIGHT="\033[1m"
RESET="\033[0m"
CLEAR="\033[2J\033[H"
cols, rows = shutil.get_terminal_size()
cols = min(cols,80)
rows = min(rows,24)
charset="01010101010101ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*"
log_height = 8
bg_rows = rows - log_height
running = True
stdout_lock = threading.Lock()
log = []

def rain_loop(density=0.09,frame_delay=0.07):
    while running:
        with stdout_lock:
            for r in range(1,bg_rows+1):
                line_chars=[]
                for c in range(cols):
                    if random.random()<density:
                        ch=random.choice(charset)
                        if random.random()<0.18:
                            line_chars.append(f"{GREEN}{BRIGHT}{ch}{RESET}")
                        else:
                            line_chars.append(f"{DIM_GREEN}{ch}{RESET}")
                    else:
                        line_chars.append(" ")
                sys.stdout.write(f"\033[{r};1H{''.join(line_chars)}")
            sys.stdout.flush()
        time.sleep(frame_delay)
def redraw_log():
    with stdout_lock:
        start_row = bg_rows+1
        visible=log[-log_height:]
        for i in range(log_height):
            row=start_row+i
            text=visible[i] if i<len(visible) else ""
            sys.stdout.write(f"\033[{row};1H{GREEN}{BRIGHT}{text.ljust(cols)}{RESET}")
        sys.stdout.flush()
def add_log(text):
    for line in text.split("\n"):
        log.append(line)
    redraw_log()
def matrix_drop(text,drop_speed=0.005):
    display=[" "]*len(text)
    base_row=bg_rows+1
    for i,ch in enumerate(text):
        display[i]=ch
        add_log("".join(display))#LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
player={"hp":25,"max_hp":25,"strength":1,"speed":1,"charm":1,"items":[],"flags":{"meatloaf_defeated":False,"toilet_defeated":False,"principal_defeated":False,"cafeteria_done":False,"gym_done":False,"auditorium_done":False,"lab_done":False,"bathroom_done":False,"library_done":False,"detention_done":False}}
def increase_stat(stat,amt):
    player[stat]+=amt
    add_log(f"Your {stat} increased by +{amt}! Now at {player[stat]}.")
def pickup_item(item):
    if item not in player["items"]:
        player["items"].append(item)
        add_log(f"Picked up: {item}!")
    else:
        add_log(f"You already have: {item}")

def show_stats():
    add_log(f"HP: {player['hp']}/{player['max_hp']}")
    add_log(f"Strength: {player['strength']}")
    add_log(f"Speed: {player['speed']}")
    add_log(f"Charm: {player['charm']}")
    add_log("Items: "+(", ".join(player["items"]) if player["items"] else "None"))

def combat(enemy):
    add_log(f"Combat started against: {enemy['name']}")
    enemy_hp=enemy["hp"]
    while player["hp"]>0 and enemy_hp>0:
        add_log(f"Your HP: {player['hp']} | {enemy['name']} HP: {enemy_hp}")
        choice=input("Attack(a)/Dodge(d)/Item(i)? ").strip().lower()
        if choice=="a":
            dmg=random.randint(1,3)+player["strength"]
            enemy_hp-=dmg
            add_log(f"You strike {enemy['name']} for {dmg}!")
        elif choice=="d":
            if random.random()<0.3+player["speed"]*0.1:
                add_log("You dodged the attack!")
                continue
            else:
                add_log("Dodge failed!")
        elif choice=="i":
            if "Burrito of Destiny" in player["items"]:
                add_log("You use Burrito of Destiny for 10 damage!")
                enemy_hp-=10
                player["items"].remove("Burrito of Destiny")
            else:
                add_log("No usable items!")
        if enemy_hp>0:
            if random.random()<0.8:
                hit=enemy["attack"]
                player["hp"]-=hit
                add_log(f"{enemy['name']} hits you for {hit}!")
            else:
                add_log(f"{enemy['name']} missed!")
    if player["hp"]<=0:
        add_log("You died.")
        return False
    else:
        add_log(f"{enemy['name']} defeated!")
        return True

# Hallway/Rooms
def cafeteria():
    add_log("=== CAFETERIA ===")
    if not player["flags"]["cafeteria_done"]:
        add_log("A Meatloaf Titan attacks you")
        titan={"name":"Meatloaf Titan","hp":18,"attack":3}
        if combat(titan):
            add_log("You defeated the Meatloaf Titan")
            pickup_item("Burrito of Destiny")
            pickup_item("Golden Hall Pass")
            increase_stat("strength",1)
            player["flags"]["meatloaf_defeated"]=True
        else:
            add_log("You were defeated")
        player["flags"]["cafeteria_done"]=True
    else:
        add_log("Nothing new here")

def hallway():
    add_log("=== HALLWAY ===")
    show_stats()
    rooms=["cafeteria","gym","auditorium","lab","library","bathroom"]
    if "Golden Hall Pass" in player["items"]:
        rooms.append("detention")
    if player["flags"]["meatloaf_defeated"]:
        rooms.append("principal_office")
    add_log("Available rooms: "+", ".join(rooms))
    choice=input("Choose a location: ").strip().lower()
    if choice in rooms:
        globals()[choice]()
    else:
        add_log("Invalid room")

def reset_game():
    player["hp"]=player["max_hp"]
    player["items"].clear()
    player["strength"]=1
    player["speed"]=1
    player["charm"]=1
    for k in player["flags"]:
        player["flags"][k]=False

def main():
    t=threading.Thread(target=rain_loop,daemon=True)
    t.start()
    add_log("SYSTEM BOOTING")
    time.sleep(0.3)
    add_log("WELCOME TO SIGMA HIGH")
    while True:
        hallway()
        if player["hp"]<=0:
            again=input("Play again? (y/n)? ").strip().lower()
            if again=="y":
                reset_game()
                continue
            else:
                break

if __name__=="__main__":
    try:
        main()
    finally:
        running=False
        time.sleep(0.1)
        with stdout_lock:
            sys.stdout.write(CLEAR)
            sys.stdout.flush()
