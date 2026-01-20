
import random   
choices = ["rock", "paper", "scissors"]
score = {"wins": 0, "losses": 0, "ties": 0}
print("Welcome to Rock, Paper, Scissors!")
print("Type 'quit' anytime to stop playing.\n")
while True:
    player = input("Choose rock, paper, or scissors: ").strip().lower()
    if player == "quit":
        print("\nFinal Scoreboard:")
        print(f"Wins: {score['wins']}, Losses: {score['losses']}, Ties: {score['ties']}")
        print("Thanks for playing! Goodbye ")
        break
    if player not in choices:
        print(" Invalid choice! Please type rock, paper, or scissors.\n")
        continue
    computer = random.choice(choices)
    print(f"Computer chose: {computer}")
    if player == computer:
        print("It's a tie! \n")
        score["ties"] += 1
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        print("You win! \n")
        score["wins"] += 1
    else:
        print("You lose! \n")
        score["losses"] += 1
    print(f"Score -> Wins: {score['wins']} | Losses: {score['losses']} | Ties: {score['ties']}\n")
