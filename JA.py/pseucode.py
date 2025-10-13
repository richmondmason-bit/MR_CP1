#Tic-Tac-Toe game
board = {
    "top-L": " ", "top-M": " ", "top-R": " ",
    "mid-L": " ", "mid-M": " ", "mid-R": " ",
    "low-L": " ", "low-M": " ", "low-R": " "
}
print("Welcome to Tic-Tac-Toe!")
print("Positions are: top-L, top-M, top-R, mid-L, mid-M, mid-R, low-L, low-M, low-R")
print("Player X goes first.")
current_player = "X"
move_count = 0
while True:
    print()
    print(f"{board['top-L']}|{board['top-M']}|{board['top-R']}")
    print("-+-+-")
    print(f"{board['mid-L']}|{board['mid-M']}|{board['mid-R']}")
    print("-+-+-")
    print(f"{board['low-L']}|{board['low-M']}|{board['low-R']}")
    print()
    move = input(f"Player {current_player}, enter your move: ")
    if move not in board:
        print("Invalid position. Please try again.")
        continue
    if board[move] != " ":
        print("That spot is already taken. Please try again.")
        continue
    board[move] = current_player
    move_count += 1
    win = False
    if board["top-L"] == current_player and board["top-M"] == current_player and board["top-R"] == current_player:
        win = True
    if board["mid-L"] == current_player and board["mid-M"] == current_player and board["mid-R"] == current_player:
        win = True
    if board["low-L"] == current_player and board["low-M"] == current_player and board["low-R"] == current_player:
        win = True
    # Columns
    if board["top-L"] == current_player and board["mid-L"] == current_player and board["low-L"] == current_player:
        win = True
    if board["top-M"] == current_player and board["mid-M"] == current_player and board["low-M"] == current_player:
        win = True
    if board["top-R"] == current_player and board["mid-R"] == current_player and board["low-R"] == current_player:
        win = True
    # Diagonals
    if board["top-L"] == current_player and board["mid-M"] == current_player and board["low-R"] == current_player:
        win = True
    if board["top-R"] == current_player and board["mid-M"] == current_player and board["low-L"] == current_player:
        win = True
    if win:
        print()
        print(f"{board['top-L']}|{board['top-M']}|{board['top-R']}")
        print("-+-+-")
        print(f"{board['mid-L']}|{board['mid-M']}|{board['mid-R']}")
        print("-+-+-")
        print(f"{board['low-L']}|{board['low-M']}|{board['low-R']}")
        print()
        print(f"Player {current_player} wins! Congratulations!")
        break
    if move_count == 9:
        print()
        print(f"{board['top-L']}|{board['top-M']}|{board['top-R']}")
        print("-+-+-")
        print(f"{board['mid-L']}|{board['mid-M']}|{board['mid-R']}")
        print("-+-+-")
        print(f"{board['low-L']}|{board['low-M']}|{board['low-R']}")
        print()
        print("It's a tie!")
        break
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"