import random
def start_game():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    number_to_guess = random.randint(1, 100)
    max_attempts = 10
    attempts = 0
    game_over = False
    while not game_over:
        guess = input("Enter your guess: ")
        if attempts >= max_attempts:
            print(f"Sorry, you've used all {max_attempts} attempts. The number was {number_to_guess}.")
            game_over = True
        if guess == number_to_guess:
            print("Congratulations! You've guessed the number!")
            game_over = True
        elif guess > number_to_guess:
            print("Too high! Try again.")
        elif guess < number_to_guess:
            print("Too low! Try again.")  
        continue
    print("Game Over. Thanks for playing!")
start_game()


#Type mismatch: input() returns a string, so guess == number_to_guess will never be True unless you convert guess to an int.

#Attempts counter: You define attempts but never increment it inside the loop.

#Game logic order: You should check if the guess is correct before checking attempts, otherwise it can print “out of attempts” even if the last guess was correct.

#continue issue: You don’t actually need continue at the end—it just restarts the loop unnecessarily.