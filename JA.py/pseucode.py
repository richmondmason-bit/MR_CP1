
#FUNCTION print_board(board)
    #FOR each row IN board
        #PRINT row with separators
        #PRINT separator line

#FUNCTION check_winner(board, player)
    #FOR i FROM 0 TO 2
        #IF all cells in row i are player
            #RETURN True
        #IF all cells in column i are player
           # RETURN True
    #IF all cells in main diagonal are player
        #RETURN True
    #IF all cells in anti-diagonal are player
        #RETURN True
    #RETURN False

#FUNCTION is_full(board)
    #RETURN True IF all cells are not empty

#FUNCTION tictactoe()
    #INITIALIZE 3x3 board with empty cells
    #SET current_player TO "X"
    #LOOP forever
        #CALL print_board(board)
        #TRY
            #GET row and col input from user
            #IF board[row][col] is not empty
                #PRINT error and CONTINUE
        #EXCEPT invalid input
            #PRINT error and CONTINUE
        #SET board[row][col] TO current_player
        #IF check_winner(board, current_player)
            #CALL print_board(board)
            #PRINT winner message
            #BREAK loop
        #IF is_full(board)
            #CALL print_board(board)
            #PRINT draw message
            #BREAK loop
        #SWITCH current_player between "X" and "O"

#IF this file is main program
    #CALL tictactoe()
