

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


